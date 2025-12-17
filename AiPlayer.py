from BasePlayer import BasePlayer
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy


def evaluate_board(board, player):
    value = 0
    for pos, owner in numpy.ndenumerate(board.owner):
        if owner == player:
            value += 1
        elif owner != 0:
            value -= 1
    return value / (board.size ** 2)


class Actor(nn.Module):
    def __init__(self, board_size, hidden_size=128):
        super(Actor, self).__init__()
        # x-times-y board with values and ownership and last move
        input_size = (board_size**2)*2+2
        output_size = board_size**2
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x, mask=None):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        logits = self.fc3(x)
        probs = F.softmax(logits, dim=-1)
        if mask is not None:
            probs = probs * mask
            probs = probs / probs.sum(dim=-1, keepdim=True)
        return probs


class AiPlayer(BasePlayer):

    class DataPoint:
        def __init__(self, log_prob, entropy):
            self.log_prob = log_prob
            self.reward = 0
            self.entropy = entropy


    def __init__(self):
        super().__init__()
        self.actor = None
        self.optimizer = None
        self.trajectory = []
        self.number_moves_won = []

    def set_config(self, config):
        super().set_config(config)
        self.actor = Actor(self.config.board_size)
        self.optimizer = optim.Adam(self.actor.parameters(), lr=self.config.Ai.learn_rate)
        self.trajectory = []
        self.number_moves_won = []


    @staticmethod
    def encode_board(player, board, last_move):
        flat_board = []
        for pos, owner in numpy.ndenumerate(board.owner):
            normalized_value = board.board[pos] / board.neighbors(pos)
            flat_board.append(normalized_value)
            normalized_owner = 0.0
            if owner == player:
                normalized_owner = 1.0
            elif owner != 0:
                normalized_owner = -1.0
            flat_board.append(normalized_owner)
        normalized_x = -1.0
        normalized_y = -1.0
        if last_move is not None:
            normalized_x = last_move[0] / (board.size - 1)
            normalized_y = last_move[1] / (board.size - 1)
        flat_board.append(normalized_x)
        flat_board.append(normalized_y)
        return torch.tensor(flat_board, dtype=torch.float32)

    def pre_game_action(self, player, board):
        super().pre_game_action(player, board)
        self.trajectory = []

    def mean_moves(self):
        if self.number_moves_won:
            return sum(self.number_moves_won) / len(self.number_moves_won)
        else:
            return self.move_number

    def beta(self):
        b_lo = self.config.Ai.beta[0]
        b_hi = self.config.Ai.beta[1]
        onset = self.config.Ai.beta_onset
        cutoff = self.config.Ai.beta_cutoff
        win_ratio = self.win_ratio()
        if win_ratio < onset:
            return b_hi
        elif win_ratio > cutoff:
            return b_lo
        else:
            factor = (win_ratio - onset) / (cutoff - onset)
            return b_lo + (b_hi - b_lo) * factor

    def post_game_action(self, player, board):
        super().post_game_action(player, board)
        if board.won():
            final_reward, reward_ratio = self.config.Ai.reward_won
            final_reward *= (self.mean_moves() / self.move_number) ** self.config.Ai.fast_game_weight
            self.number_moves_won += [self.move_number]
        else:
            final_reward, reward_ratio = self.config.Ai.reward_lost
        losses = []
        for p in self.trajectory:
            combined_reward = final_reward + p.reward * reward_ratio
            loss = (-p.log_prob * combined_reward) - self.beta() * p.entropy
            losses.append(loss)
        loss = torch.stack(losses).sum()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def ai_evaluate_last_move(self, player, board, last_move):
        if self.trajectory:
            reward = evaluate_board(board, player)
            self.trajectory[-1].reward = reward

    def ai_move(self, player, board, last_move):
        state = self.encode_board(player, board, last_move)
        probs = self.actor(state, torch.from_numpy(self.possible_mask))
        dist = torch.distributions.Categorical(probs)
        action = dist.sample().item()
        log_prob = dist.log_prob(torch.tensor(action))
        self.trajectory.append(self.DataPoint(log_prob, dist.entropy().mean()))
        return action

    def next_move(self, player, board, last_move):
        self.ai_evaluate_last_move(player, board, last_move)
        super().next_move(player, board, last_move)
        action = self.ai_move(player, board, last_move)
        pos = board.idx2pos(action)
        return pos

