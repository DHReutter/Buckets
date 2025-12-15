from GameBoard import GameBoard


class GameSimulation:
    def __init__(self, config):
        self.config = config
        self.board = None
        self.last_player = None
        self.current_player = None
        self.last_move = None
        self.exploding = False
        self.scored = False
        self.score = {1: 0, 2: 0}
        self.reset()

    def reset(self, start_player=1):
        self.board = GameBoard(self.config.board_size)
        self.last_player = 0
        self.current_player = start_player
        self.config.player[start_player].pre_game_action(start_player, self.board)
        self.config.player[3-start_player].pre_game_action(3-start_player, self.board)
        self.last_move = None
        self.exploding = False
        self.scored = False

    def number_games(self):
        return self.score[1] + self.score[2]

    def win_loss_ratio(self, player):
        return self.score[player] / self.number_games()

    def game_over(self):
        if not self.scored and not self.board.is_ongoing():
            self.scored = True
            winner = self.board.won()
            self.score[winner] += 1
            self.config.player[winner].post_game_action(winner, self.board)
            self.config.player[3-winner].post_game_action(3-winner, self.board)
        return not self.board.is_ongoing()

    def continue_spill(self):
        if self.exploding:
            self.board.spill_once(self.last_player)
            self.exploding = self.board.determine_spills().any()
        return self.exploding

    def make_move(self, pos):
        self.board.place(self.current_player, pos)
        self.last_player = self.current_player
        self.current_player = 3 - self.current_player
        self.last_move = pos
        self.exploding = self.board.determine_spills().any()

    def make_ai_move(self):
        if not self.game_over():
            self.make_move(self.config.player[self.current_player].next_move(self.current_player, self.board,
                                                                             self.last_move))

    def print_board(self):
        print(f"Running: {self.board.is_ongoing()}")
        print(f"Current Player: {self.current_player}")
        self.board.print()


def simulate_game(config, repetitions=1, alternate_players=False):
    game = GameSimulation(config)
    start_player = 1
    rolling_mean = [0.0] * 100
    for i in range(0, repetitions):
        print(f"Game #{i+1} of {repetitions}, Player #{start_player} begins", end=" ")
        while not game.game_over():
            print(".", end="")
            while game.continue_spill() and not game.game_over():
                pass
            game.make_ai_move()
        rolling_mean[i % 100] = game.win_loss_ratio(1)
        print(f"Player #{game.board.won()} won ({round(sum(rolling_mean), 1)}%).")
        if alternate_players:
            start_player = 3 - start_player
        game.reset(start_player=start_player)
    print(game.score)
