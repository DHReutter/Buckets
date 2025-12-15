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
    def __init__(self, board_size):
        super().__init__()
        self.board_size = board_size
        self.actor = Actor(board_size)
        self.optimizer = optim.Adam(self.actor.parameters(), lr=0.001)
        self.trajectory = {}

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
        self.trajectory = {}

    def post_game_action(self, player, board):
        final_reward = 1.0 if board.won() == player else -1.0
        losses = []
        for log_prob, reward in self.trajectory.items():
            losses.append(-log_prob * (reward + final_reward))
        loss = torch.stack(losses).sum()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def ai_evaluate_last_move(self, player, board, last_move):
        if self.trajectory:
            last_log_prob = list(self.trajectory.keys())[-1]
            reward = evaluate_board(board, player) * 0.1
            self.trajectory[last_log_prob] = reward

    def ai_move(self, player, board, last_move):
        state = self.encode_board(player, board, last_move)
        probs = self.actor(state, torch.from_numpy(self.possible_mask))
        dist = torch.distributions.Categorical(probs)
        action = dist.sample().item()
        log_prob = dist.log_prob(torch.tensor(action))
        self.trajectory[log_prob] = 0
        return action

    def next_move(self, player, board, last_move):
        self.ai_evaluate_last_move(player, board, last_move)
        super().next_move(player, board, last_move)
        action = self.ai_move(player, board, last_move)
        pos = board.idx2pos(action)
        return pos

