from BasePlayer import BasePlayer


class HumanPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.human = True
