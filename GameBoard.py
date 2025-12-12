import numpy


class GameBoard:
    def __init__(self, size):
        self.size = size
        self.board = numpy.zeros((size, size), dtype=numpy.uint8)
        self.owner = numpy.zeros((size, size), dtype=numpy.uint8)
        self.place(1, (0, 0))
        self.place(2, (size - 1, size - 1))

    def legal_position(self, pos):
        return all(0 <= x < self.size for x in pos)

    def placeable(self, player, pos):
        assert(self.legal_position(pos))
        return self.owner[pos] == 0 or self.owner[pos] == player

    def place(self, player, pos):
        assert(self.placeable(player, pos))
        self.board[pos] = self.board[pos] + 1
        self.owner[pos] = player

    def neighbors(self, pos):
        x = pos[0]
        y = pos[1]
        x_border = False
        y_border = False
        if x == 0 or x == self.size-1:
            x_border = True
        if y == 0 or y == self.size-1:
            y_border = True
        return 4 - x_border - y_border

    def neighbor_positions(self, pos):
        positions = []
        for operation in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            candidate = tuple(numpy.add(pos, operation))
            if self.legal_position(candidate):
                positions.append(candidate)
        return positions

    def determine_spills(self):
        spilling = numpy.zeros((self.size, self.size), dtype=numpy.bool)
        for pos, value in numpy.ndenumerate(self.board):
            spilling[pos] = value >= self.neighbors(pos)
        return spilling

    def spill_once(self, player):
        # Determine where to spill
        spilling = self.determine_spills()
        # No spilling? Quit.
        if not spilling.any():
            return False
        # Spill.
        for pos, spilled in numpy.ndenumerate(spilling):
            if spilled:
                for neighbor_pos in self.neighbor_positions(pos):
                    self.board[neighbor_pos] = self.board[neighbor_pos] + 1
                    self.owner[neighbor_pos] = player
                self.board[pos] -= self.neighbors(pos)
                if self.board[pos] == 0:
                    self.owner[pos] = 0
        return True

    def won(self):
        if (self.owner != 1).all():
            return 2
        elif (self.owner != 2).all():
            return 1
        else:
            return 0

    def is_ongoing(self):
        return self.won() == 0

    def print(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                print(f"{self.owner[(x, y)]}:{self.board[(x, y)]} ", end="")
            print("\n")
