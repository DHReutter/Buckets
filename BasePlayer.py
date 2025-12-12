import numpy


class BasePlayer:
    def __init__(self):
        self.possible_plays = []
        self.possible_mask = None
        pass

    def set_possible_plays(self, player, board):
        self.possible_plays = []
        if self.possible_mask is None:
            self.possible_mask = numpy.zeros(board.owner.size, dtype=numpy.bool)
        i = 0
        for pos, owner in numpy.ndenumerate(board.owner):
            if owner == 0 or owner == player:
                self.possible_plays.append(pos)
                self.possible_mask[i] = True
            else:
                self.possible_mask[i] = False
            i += 1

    def next_move(self, player, board, last_move):
        self.set_possible_plays(player, board)
