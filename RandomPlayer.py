import numpy
import random


class RandomPlayer:

    def __init__(self):
        pass

    @staticmethod
    def next_move(player, board, _):
        possible_plays = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == 0 or owner == player]
        return random.choice(possible_plays)
