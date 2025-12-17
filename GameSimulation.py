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
        for p in self.config.player.values():
            p.set_config(self.config)

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


def simulate_game(config):
    game = GameSimulation(config)
    start_player = 1
    rolling_mean = [0.0] * 100

    alternate_players = False
    if 'alternate_players' in dir(config.Simulation):
        alternate_players = config.Simulation.alternate_players
    repetitions = 1
    if 'repetitions' in dir(config.Simulation):
        repetitions = config.Simulation.repetitions
    target_rate = None
    if 'target_rate' in dir(config.Simulation):
        target_rate = config.Simulation.target_rate
        repetitions = f"TR{round(target_rate * 100, 1)}%"
    running = True
    i = 0
    while running:
        print(f"Game #{i+1} of {repetitions}, Player #{start_player} begins", end="... ")
        while not game.game_over():
            while game.continue_spill() and not game.game_over():
                pass
            game.make_ai_move()
        # Next game
        rolling_mean[i % 100] = game.win_loss_ratio(1)
        mean_win_rate = sum(rolling_mean) / len(rolling_mean)
        i += 1
        target_rate_str = ""
        if target_rate:
            if mean_win_rate > target_rate:
                running = False
        elif i >= repetitions:
            running = False
        number_moves_str = str(config.player[1].move_number)
        win_loss_str = "won " if game.board.won() == 1 else "lost"
        win_rate_str = str(round(config.player[1].win_ratio() * 100, 1)) + "%"
        rolling_mean_str = str(round(mean_win_rate * 100, 1)) + "%"
        print(f"AI {win_loss_str} after {number_moves_str} moves [{win_rate_str} - {rolling_mean_str}]")
        if alternate_players:
            start_player = 3 - start_player
        game.reset(start_player=start_player)
    print(game.score)
