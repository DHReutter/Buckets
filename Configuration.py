from RandomPlayer import RandomPlayer
from AiPlayer import AiPlayer


class Configuration:
    board_size = 6
    font_name = 'Consolas'
    font_size = 24
    field_size_px = (48, 64)
    player_colors = {1: "orange", 2: "lightblue"}
    fps = 60
    explosion_frames = 20
    player = {1: AiPlayer(), 2: RandomPlayer()}
    sound = False

    class Simulation:
        alternate_players = True
        target_rate = 0.75

    class Ai:
        learn_rate = 0.0005
        reward_won = (1.0, 0.1)
        reward_lost = (-1.0, 0.1)
        fast_game_weight = 4
        beta_onset = 0.5
        beta_cutoff = 0.7
        beta = (0.05, 0.001)
