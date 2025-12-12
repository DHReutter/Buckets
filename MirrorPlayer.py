import numpy
import random
from BasePlayer import BasePlayer


class MirrorPlayer(BasePlayer):

    def __init__(self):
        super().__init__()
        pass

    def next_move(self, player, board, last_move):
        super().next_move(player, board, last_move)
        if last_move is None:
            return random.choice(self.possible_plays)
        else:
            move = (board.size - 1 - last_move[0], board.size - 1 - last_move[1])
            if move in self.possible_plays:
                return move
            else:
                return random.choice(self.possible_plays)
