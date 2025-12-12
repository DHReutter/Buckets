from GameBoard import GameBoard


class GameSimulation:
    def __init__(self, config):
        self.config = config
        self.board = None
        self.last_player = None
        self.current_player = None
        self.last_move = None
        self.scored = False
        self.score = {1: 0, 2:0}
        self.reset()

    def reset(self):
        self.board = GameBoard(self.config.board_size)
        self.last_player = 0
        self.current_player = 1
        self.scored = False
        self.last_move = None

    def game_over(self):
        if not self.scored and not self.board.is_ongoing():
            self.scored = True
            self.score[self.board.won()] += 1
        return not self.board.is_ongoing()

    def make_move(self, pos):
        self.board.place(self.current_player, pos)
        self.last_player = self.current_player
        self.current_player = 3 - self.current_player
        self.last_move = pos

    def make_ai_move(self):
        if not self.game_over():
            self.make_move(self.config.player[self.current_player].next_move(self.current_player, self.board,
                                                                             self.last_move))
