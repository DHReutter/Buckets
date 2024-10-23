import numpy
import random


class FillAndAttackPlayer:

    def __init__(self, randomize=0):
        self.randomize = randomize

    @staticmethod
    def dangerous(pos, player, board):
        distance = board.neighbors(pos) - board.board[pos]
        for n in board.neighbor_positions(pos):
            if board.neighbors(pos) - board.board[n] < distance and board.owner[n] != player:
                return True
        return False

    def next_move(self, player, board, _):
        if random.random() < self.randomize:
            print("Random move! Haha!")
            return random.choice([pos for pos, owner in numpy.ndenumerate(board.owner)
                                  if owner == 0 or owner == player])
        own_plays = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == player]
        random.shuffle(own_plays)
        # See if one could explode
        for possible_play in own_plays:
            if board.board[possible_play] + 1 == board.neighbors(possible_play):
                print("Possible spilling at {possible_play}")
                for neighbor in board.neighbor_positions(possible_play):
                    if board.owner[neighbor] != 0 and board.owner[neighbor] != player:
                        print("ATTACKING!")
                        return possible_play
        # See if it could be raised
        sensible_plays = [pos for pos in own_plays if not FillAndAttackPlayer.dangerous(pos, player, board)]
        for possible_play in sensible_plays:
            if board.board[possible_play] < board.neighbors(possible_play) - 1:
                print(f"Raising ...")
                return possible_play
        # No raise and no viable explosion: Select a neighboring field
        for possible_play in sensible_plays:
            for neighbor in board.neighbor_positions(possible_play):
                if board.owner[neighbor] == 0:
                    print("Growing ...")
                    return neighbor
        # No neighboring field either, just select an empty one.
        empty_fields = [pos for pos, owner in numpy.ndenumerate(board.owner) if owner == 0]
        if len(empty_fields) == 0:
            print("No empty fields.")
            return random.choice(own_plays)
        else:
            print("Selecting empty field.")
            return random.choice(empty_fields)

