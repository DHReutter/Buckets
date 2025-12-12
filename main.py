from GameSimulation import simulate_game
# from GamePlay import play_game
from RandomPlayer import RandomPlayer
# import FillAndAttackPlayer
# import MirrorPlayer


class Configuration:
    board_size = 6
    font_name = 'Consolas'
    font_size = 24
    field_size_px = (48, 64)
    player_colors = {1: "orange", 2: "lightblue"}
    fps = 60
    explosion_frames = 20
    player = {1: RandomPlayer(), 2: RandomPlayer()}
    sound = False


if __name__ == '__main__':
    simulate_game(Configuration, 200, True)
    exit(0)
