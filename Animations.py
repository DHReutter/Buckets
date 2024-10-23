import numpy
import pygame


class ExplodeAnimation:

    def __init__(self, steps):
        self.step = 0
        self.max_steps = steps

    def draw(self, game_board, surface, field_size):
        explosion = pygame.Surface(field_size)
        pygame.draw.circle(explosion, "blue", numpy.divide(field_size, 2),
                           self.step * min(field_size) / self.max_steps - 5)
        pygame.draw.circle(explosion, "black", numpy.divide(field_size, 2),
                           self.step * min(field_size) / self.max_steps - 8)
        for position in (p for p, spilling in numpy.ndenumerate(game_board.determine_spills()) if spilling):
            surface.blit(explosion, tuple(numpy.multiply(position, field_size)))
        self.step = self.step + 1
        return self.step < self.max_steps
