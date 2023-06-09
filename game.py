"""
Game module is responsible for running the game main loop,
displaying objects and counters on screen and handling user inputs
"""

import threading
import pygame
import random
from window import Window
from score import Score
from vegetable import Vegetable
from timer import Timer
from universal_generator import UniversalGenerator
from bomb import Bomb


class Game:

    def __init__(self):
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

        self.releas_position = (self.window.screen.get_size()[0] * 0.5,
                                self.window.screen.get_size()[1] * 0.5)
        # generators
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
        self.window.resize((640, 480))
        self.start_threads()

        while not self.event_handler():
            self.window.draw_background()

            # Display timer
            timer_text = pygame.font.Font(None, 50) \
                .render("{:02d}:{:02d}" \
                        .format(self.timer.game_time//60, self.timer.game_time % 60),True,(255, 255, 255))
            timer_rect = timer_text.get_rect(center=self.timer_position)
            self.window.screen.blit(timer_text, timer_rect)

            if self.display_alert:
                release_text = pygame.font.Font(None, 50) \
                    .render("Release the left button", True, (255, 255, 255))
                release_rect = release_text.get_rect(center=self.releas_position)
                self.window.screen.blit(release_text, release_rect)

            # Display score
            score_text = pygame.font.Font(None, 50)\
                .render("Score: {}".format(self.score.total_score), True, (255, 255, 255))
            score_rect = timer_text.get_rect(center=self.score_position)
            self.window.screen.blit(score_text, score_rect)

            # Display vegetable
            self.vegetable_group.update(random.uniform(1, 2), self.window.screen)
            self.vegetable_group.draw(self.window.screen)
            self.vegetable_group.add(self.veg_gen.get_objects())
            self.veg_gen.clear_objects()

            # Display Bomb
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

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            # ! needs to be fixed
            elif event.type == pygame.VIDEORESIZE:
                self.window.resize(event.size)
                # raise NotImplementedError
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.is_mouse_down = True
                if self.first_press:
                    self.slash_sound.play(0)
                    self.first_press = False
                    self.button_press_time = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.button_press_time = 0
                self.display_alert = False
                self.first_press = True
                self.is_mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                if self.is_mouse_down and (pygame.time.get_ticks() - self.button_press_time) < 400:
                    for veg in self.vegetable_group:
                        if veg.rect.collidepoint(pygame.mouse.get_pos()):
                            # self.slash_sound.play(0)
                            threading.Thread(target=self.score.add_point, daemon=True).start()
                            self.vegetable_group.remove(veg)
                            veg.kill()
                            if (self.score.total_score != 0 and self.score.total_score % 10 == 0):
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
        self.timer_thread.start()
        self.score_thread.start()
        self.veg_gen_thread.start()
        self.bomb_gen_thread.start()
