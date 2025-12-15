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
    player = {1: AiPlayer(board_size), 2: RandomPlayer()}
    sound = False
