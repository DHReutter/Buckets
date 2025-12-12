import numpy
import random
from BasePlayer import BasePlayer


class RandomPlayer(BasePlayer):

    def __init__(self):
        super().__init__()
        pass

    def next_move(self, player, board, last_move):
        super().next_move(player, board, last_move)
        return random.choice(self.possible_plays)
