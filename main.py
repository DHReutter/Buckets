from GameSimulation import simulate_game
from GamePlay import play_game
from Configuration import Configuration
from HumanPlayer import HumanPlayer

if __name__ == '__main__':
    config = Configuration
    simulate_game(config, 1000, True)
    config.player[2] = HumanPlayer()
    play_game(config)
    exit(0)
