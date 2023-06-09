"""
game.py

This module is responsible for running the game main loop, displaying objects
and counters on the screen, and handling user inputs.
"""
import threading
import random
import pygame
from window import Window
from score import Score
from vegetable import Vegetable
from timer import Timer
from universal_generator import UniversalGenerator
from bomb import Bomb


class Game:
    """
    The Game class represents the game instance.

    Attributes:
        window (Window): The game window object.
        clock (pygame.time.Clock): The pygame clock object for controlling the frame rate.
        vegetable (Vegetable): The vegetable object.
        ...
        
    Methods:
        start: Starts the game loop.
        event_handler: Handles game events.
        start_threads: Starts the game-related threads.
    """

    def __init__(self):
        """
        Initializes a Game instance.
        """
        pygame.init()
        self.window = Window(640, 480)
        self.clock = pygame.time.Clock()
        self.vegetable = Vegetable(self.window.screen.get_size())
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/Naruto - Fight.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)
        self.slash_sound = pygame.mixer.Sound("sounds/slash.wav")
        self.slash_sound.set_volume(0.2)
        self.power_up = pygame.mixer.Sound('sounds/level_up.mp3')
        self.power_up.set_volume(0.2)
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')
        self.explosion_sound.set_volume(0.3)
        self.vegetable_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()

        self.timer = Timer(120)
        self.timer_thread = threading.Thread(target=self.timer.run_timer, daemon=True)
        self.timer_position = tuple(value * 0.1 for value in self.window.screen.get_size())

        self.score = Score()
        self.score_thread = threading.Thread(target=self.score.run_score, daemon=True)
        self.score_position = (self.window.screen.get_size()[0] * 0.80,
                               self.window.screen.get_size()[1] * 0.1)

        self.release_position = (self.window.screen.get_size()[0] * 0.5,
                                self.window.screen.get_size()[1] * 0.5)
        self.veg_gen = UniversalGenerator(self.window, Vegetable)
        self.veg_gen_thread = threading.Thread(target=self.veg_gen.run_generator, daemon=True)
        self.bomb_gen = UniversalGenerator(self.window, Bomb, (3, 8), (1, 3))
        self.bomb_gen_thread = threading.Thread(target=self.bomb_gen.run_generator, daemon=True)
        self.slices = []
        self.is_mouse_down = False
        self.animation_duration = 0.2
        self.button_press_time = 0
        self.first_press = True
        self.display_alert = False

    def start(self):
        """
        Starts the game loop.
        
        Returns:
            bool: True if the game loop should exit, False otherwise.
        """
        self.window.resize((640, 480))
        self.start_threads()

        while not self.event_handler():
            self.window.draw_background()

            white = (255, 255, 255)
            minutes = self.timer.game_time // 60
            seconds = self.timer.game_time % 60
            timer_text = pygame.font.Font(None, 50) \
                .render(f"{minutes:02d}:{seconds:02d}", True, white)
            timer_rect = timer_text.get_rect(center=self.timer_position)
            self.window.screen.blit(timer_text, timer_rect)

            if self.display_alert:
                white = (255, 255, 255)
                release_text = pygame.font.Font(None, 50) \
                    .render("Release the left button", True, white)
                release_rect = release_text.get_rect(center=self.release_position)
                self.window.screen.blit(release_text, release_rect)

            score_text = pygame.font.Font(None, 50) \
                .render(f"Score: {self.score.total_score}", True, white)
            score_rect = timer_text.get_rect(center=self.score_position)
            self.window.screen.blit(score_text, score_rect)

            self.vegetable_group.update(random.uniform(1, 2), self.window.screen)
            self.vegetable_group.draw(self.window.screen)
            self.vegetable_group.add(self.veg_gen.get_objects())
            self.veg_gen.clear_objects()

            self.bomb_group.update(random.uniform(1.3, 2.6), self.window.screen)
            self.bomb_group.draw(self.window.screen)
            self.bomb_group.add(self.bomb_gen.get_objects())
            self.bomb_gen.clear_objects()

            self.clock.tick(144)
            # ! test
            if self.is_mouse_down:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.slices.append({"pos": (mouse_x, mouse_y), "timer": 0})

            for slice_data in self.slices:
                slice_pos = (
                slice_data["pos"][0] + random.randint(2, 5)
                    if random.choice([0, 1]) else slice_data["pos"][0] - random.randint(2, 5),
                slice_data["pos"][1] + random.randint(2, 5)
                    if random.choice([0, 1]) else slice_data["pos"][1] - random.randint(2, 5))
                slice_timer = slice_data["timer"]

                if slice_timer < self.animation_duration:
                    color = (0, random.randint(100, 200), 0)
                    rect = pygame.Rect(slice_pos, (random.randint(8, 15), random.randint(8, 15)))
                    pygame.draw.rect(self.window.screen, color, rect)
                    slice_data["timer"] += self.clock.get_time() / 1000
                else:
                    self.slices.remove(slice_data)
            pygame.display.flip()

            if self.timer.game_time == 0:
                pygame.quit()
                return True
        return False

    def event_handler(self):
        """
        Handle the mouse motion event.

        Args:
            event (pygame.event.Event): The pygame event object representing the mouse motion event.

        Returns:
            bool: False, indicating the event handler should not exit.
        """
        event_handlers = {
            pygame.QUIT: self.handle_quit,
            pygame.VIDEORESIZE: self.handle_resize,
            pygame.MOUSEBUTTONDOWN: self.handle_mouse_button_down,
            pygame.MOUSEBUTTONUP: self.handle_mouse_button_up,
            pygame.MOUSEMOTION: self.handle_mouse_motion,
        }

        for event in pygame.event.get():
            event_type = event.type
            if event_type in event_handlers:
                if event_handlers[event_type](event) is True:
                    return True

        return False

    def handle_quit(self, _):
        """
        Handle the quit event.

        Args:
            _ (Any): Unused argument.

        Returns:
            bool: True, indicating the event handler should exit.
        """
        pygame.quit()
        return True

    def handle_resize(self, event):
        """
        Handle the resize event.

        Args:
            event (pygame.event.Event): The pygame event object representing the resize event.

        Returns:
            bool: False, indicating the event handler should not exit.
        """
        self.window.resize(event.size)
        return False

    def handle_mouse_button_down(self, event):
        """
        Handle the mouse button down event.

        Args:
            event (pygame.event.Event): The pygame event representing the mouse button down event.

        Returns:
            bool: False, indicating the event handler should not exit.
        """
        if event.button == 1:
            self.is_mouse_down = True
            if self.first_press:
                self.slash_sound.play(0)
                self.first_press = False
                self.button_press_time = pygame.time.get_ticks()
        return False

    def handle_mouse_button_up(self, event):
        """
        Handle the mouse button up event.

        Args:
            event (pygame.event.Event): The pygame event representing the mouse button up event.

        Returns:
            bool: False, indicating the event handler should not exit.
        """
        if event.button == 1:
            self.button_press_time = 0
            self.display_alert = False
            self.first_press = True
            self.is_mouse_down = False
        return False

    def handle_mouse_motion(self, _):
        """
        Handle the mouse motion event.

        Args:
            event (pygame.event.Event): The pygame event object representing the mouse motion event.

        Returns:
            bool: False, indicating the event handler should not exit.
        """
        if self.is_mouse_down and (pygame.time.get_ticks() - self.button_press_time) < 400:
            for veg in self.vegetable_group:
                if not veg.rect.collidepoint(pygame.mouse.get_pos()):
                    continue
                threading.Thread(target=self.score.add_point, daemon=True).start()
                self.vegetable_group.remove(veg)
                veg.kill()
                if self.score.total_score != 0 and self.score.total_score % 10 == 0:
                    self.timer.start_freeze_thread()
                    self.power_up.play(0)
            for bomb in self.bomb_group:
                if bomb.rect.collidepoint(pygame.mouse.get_pos()):
                    self.slash_sound.play(0)
                    self.explosion_sound.play(0)
                    threading.Thread(target=self.score.divide_points, daemon=True).start()
                    self.bomb_group.remove(bomb)
                    bomb.kill()
        elif self.is_mouse_down:
            self.is_mouse_down = False
            self.display_alert = True
            self.button_press_time = 0
            self.first_press = True
        return False

    def start_threads(self):
        """
        Start the necessary threads for the game.

        Args:
            None

        Returns:
            None
        """
        self.timer_thread.start()
        self.score_thread.start()
        self.veg_gen_thread.start()
        self.bomb_gen_thread.start()
