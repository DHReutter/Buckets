import numpy
import random


class MirrorPlayer:

    def __init__(self):
        pass

    @staticmethod
    def next_move(player, board, last_move):
        possible_plays = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == 0 or owner == player]
        if last_move is None:
            return random.choice(possible_plays)
        else:
            move = (board.size - 1 - last_move[0], board.size - 1 - last_move[1])
            if move in possible_plays:
                return move
            else:
                return random.choice(possible_plays)
