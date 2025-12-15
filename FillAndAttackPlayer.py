import numpy
import random
from BasePlayer import BasePlayer


class FillAndAttackPlayer(BasePlayer):

    def __init__(self, randomize=0):
        super().__init__()
        self.randomize = randomize

    @staticmethod
    def dangerous(pos, player, board):
        distance = board.neighbors(pos) - board.board[pos]
        for n in board.neighbor_positions(pos):
            if board.neighbors(pos) - board.board[n] < distance and board.owner[n] != player:
                return True
        return False

    def next_move(self, player, board, last_move):
        super().next_move(player, board, last_move)
        if random.random() < self.randomize:
            return random.choice([pos for pos, owner in numpy.ndenumerate(board.owner)
                                  if owner == 0 or owner == player])
        own_plays = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == player]
        random.shuffle(own_plays)
        # See if one could explode
        for possible_play in own_plays:
            if board.board[possible_play] + 1 == board.neighbors(possible_play):
                for neighbor in board.neighbor_positions(possible_play):
                    if board.owner[neighbor] != 0 and board.owner[neighbor] != player:
                        return possible_play
        # See if it could be raised
        sensible_plays = [pos for pos in own_plays if not FillAndAttackPlayer.dangerous(pos, player, board)]
        for possible_play in sensible_plays:
            if board.board[possible_play] < board.neighbors(possible_play) - 1:
                return possible_play
        # No raise and no viable explosion: Select a neighboring field
        for possible_play in sensible_plays:
            for neighbor in board.neighbor_positions(possible_play):
                if board.owner[neighbor] == 0:
                    return neighbor
        # No neighboring field either, just select an empty one.
        empty_fields = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == 0]
        if len(empty_fields) == 0:
            return random.choice(own_plays)
        else:
            return random.choice(empty_fields)
