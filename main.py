from GamePlay import GamePlay
import RandomPlayer
import FillAndAttackPlayer
import MirrorPlayer


class Configuration:
    board_size = 6
    font_name = 'Consolas'
    font_size = 24
    field_size_px = (48, 64)
    player_colors = {1: "orange", 2: "lightblue"}
    fps = 60
    explosion_frames = 20
    player = {1: FillAndAttackPlayer.FillAndAttackPlayer(), 2: FillAndAttackPlayer.FillAndAttackPlayer()}
    sound = False


if __name__ == '__main__':
    game = GamePlay(Configuration)
    while game.running:
        # Main Loop
        game.set_name()
        game.continue_spill()
        game.event_handling()
        game.make_ai_move()
        game.draw()
    exit(0)
