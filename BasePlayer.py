import numpy


class BasePlayer:
    def __init__(self):
        self.possible_plays = []
        self.possible_mask = None
        self.human = False
        self.config = None
        self.move_number = 0
        self.games = 0
        self.wins = 0

    def set_config(self, config):
        self.config = config

    def is_human(self):
        return self.human

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
        self.move_number += 1
        self.set_possible_plays(player, board)

    def win_ratio(self):
        return self.wins / self.games if self.games else 0.0

    def pre_game_action(self, player, board):
        self.move_number = 0

    def post_game_action(self, player, board):
        self.games += 1
        if board.won() == player:
            self.wins += 1
