import numpy


class BasePlayer:
    def __init__(self):
        self.possible_plays = []
        self.possible_mask = None
        pass

    def pre_game_action(self, player, board):
        pass

    def set_possible_plays(self, player, board):
        self.possible_plays = []
        if self.possible_mask is None:
            self.possible_mask = numpy.zeros(board.size**2, dtype=numpy.bool)
        for pos, owner in numpy.ndenumerate(board.owner):
            idx = board.pos2idx(pos)
            if owner == 0 or owner == player:
                self.possible_plays.append(pos)
                self.possible_mask[idx] = True
            else:
                self.possible_mask[idx] = False

    def next_move(self, player, board, last_move):
        self.set_possible_plays(player, board)

    def post_game_action(self, player, board):
        pass
