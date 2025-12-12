import numpy


class BasePlayer:
    def __init__(self):
        self.possible_plays = []
        pass

    def set_possible_plays(self, player, board):
        self.possible_plays = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == 0 or owner == player]

    def next_move(self, player, board, last_move):
        self.set_possible_plays(player, board)
