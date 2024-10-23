import pygame
import pygame.freetype
import numpy
from TupleOperations import *
from GameBoard import GameBoard
from Animations import ExplodeAnimation
import matplotlib.pyplot as plt


def make_sound(game_board, duration):
    time = numpy.arange(0, duration, 1/pygame.mixer.get_init()[0])
    length = numpy.rint(pygame.mixer.get_init()[0] * duration).astype(int)
    print(length)
    print(len(time))
    hull = numpy.divide(numpy.arange(length), length)
    buffer = 1
    for position in (p for p, spilling in numpy.ndenumerate(game_board.determine_spills()) if spilling):
        frequency = 220 + (position[0] + position[1] * (game_board.board.shape[1])) * 220
        buffer = numpy.sin(2 * numpy.pi * time * frequency) * buffer
    # plt.plot(buffer)
    # plt.show()
    sound = pygame.mixer.Sound(buffer=buffer)
    sound.set_volume(1.0)
    sound.play()
    # for position in (p for p, spilling in numpy.ndenumerate(game_board.determine_spills()) if spilling):


class GamePlay:
    def __init__(self, config):
        # PyGame initialization.
        pygame.init()
        pygame.freetype.init()
        pygame.mixer.init(channels=4, size=16)
        # Other initializations.
        self.config = config
        self.running = True
        self.screen_size = t_mul(self.config.field_size_px, self.config.board_size)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.font = pygame.freetype.SysFont(self.config.font_name, self.config.font_size)
        self.clock = pygame.time.Clock()
        # State variables.
        self.board = None
        self.last_player = None
        self.current_player = None
        self.exploding = None
        self.animation = None
        self.message = None
        self.last_move = None
        self.reset()

    def __del__(self):
        pygame.mixer.quit()
        pygame.freetype.quit()
        pygame.quit()

    def start_animation(self, animation):
        if self.animation is not None:
            print("ERROR!")
        self.animation = animation(self.config.explosion_frames)
        if self.config.sound:
            make_sound(self.board, self.config.explosion_frames / self.config.fps)

    def stop_animation(self):
        self.animation = None
        pygame.mixer.stop()

    def reset(self):
        self.board = GameBoard(self.config.board_size)
        self.last_player = 0
        self.current_player = 1
        self.exploding = False
        self.message = None
        self.last_move = None
        self.stop_animation()
        pygame.mixer.stop()

    def set_name(self):
        if self.exploding:
            pygame.display.set_caption(f'Exploding')
        else:
            pygame.display.set_caption(f'Player {self.current_player}')

    def is_animating(self):
        return self.animation is not None

    def game_over(self):
        return not self.board.is_ongoing()

    def continue_spill(self):
        if self.exploding and not self.is_animating():
            self.board.spill_once(self.last_player)
            if self.board.determine_spills().any():
                self.start_animation(ExplodeAnimation)
            else:
                self.exploding = False

    def make_move(self, pos):
        self.board.place(self.current_player, pos)
        self.exploding = self.board.determine_spills().any()
        if self.exploding:
            self.start_animation(ExplodeAnimation)
        self.last_player = self.current_player
        self.current_player = 3 - self.current_player
        self.last_move = pos

    def event_handling(self):
        for event in pygame.event.get():
            # Quit on QUIT or q
            if event.type == pygame.QUIT or\
                    (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                self.running = False
            # Reset on r
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.reset()
            # User move, only performed when game is not running
            if not self.game_over() and not self.is_animating() and not self.exploding:
                # Click in field
                if self.config.player[self.current_player] == 'HUMAN':
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = tuple(numpy.floor(numpy.divide(pygame.mouse.get_pos(),
                                                             self.config.field_size_px)).astype(int))
                        if self.board.placeable(self.current_player, pos):
                            self.make_move(pos)
                        else:
                            self.message = "Invalid move!"
            if self.message is not None and event.type == pygame.MOUSEBUTTONUP:
                self.message = None

    def make_ai_move(self):
        if self.config.player[self.current_player] != "HUMAN":
            if not self.game_over() and not self.is_animating() and not self.exploding:
                self.make_move(self.config.player[self.current_player].next_move(self.current_player, self.board,
                                                                                 self.last_move))

    def draw(self):
        self.clock.tick(self.config.fps)
        # Draw board
        for idx, value in numpy.ndenumerate(self.board.board):
            field = pygame.Surface(self.config.field_size_px)
            field.fill("white")
            pygame.draw.rect(field, "black", pygame.Rect((1, 1), t_sub(self.config.field_size_px, 2)))
            if value > 0:
                text_size = self.font.get_rect(str(value)).size
                text_pos = tt_sub(t_mul(self.config.field_size_px, 0.5), t_mul(text_size, 0.5))
                self.font.render_to(field, text_pos, str(value),
                                    fgcolor=self.config.player_colors[self.board.owner[idx]])
            self.screen.blit(field, tt_mul(idx, self.config.field_size_px))
        # Draw Animations
        if self.is_animating():
            if not self.animation.draw(self.board, self.screen, self.config.field_size_px):
                self.stop_animation()
        # Display game over or other messages
        if self.game_over():
            self.display_message(f'Player {self.board.won()} won!', self.config.player_colors[self.board.won()])
        elif self.message is not None:
            self.display_message(self.message, "darkgrey")
        pygame.display.flip()

    def display_message(self, text, color):
        message_size = self.font.get_rect(text).size
        message_pos = tt_sub(t_mul(self.screen_size, 0.5), t_mul(message_size, 0.5))
        self.font.render_to(self.screen, message_pos, text, fgcolor=color, bgcolor='black')
