import threading
import pygame
import random
from window import Window
from score import Score
from vegetable import Vegetable
from generator import Generator
from bomb_generator import BombGenerator
from timer import Timer

class Game:

    def __init__(self):
        pygame.init()
        self.window = Window(640, 480)
        self.clock = pygame.time.Clock()
        self.vegetable = Vegetable(self.window.screen.get_size())
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/Naruto - Fight.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.slash_sound = pygame.mixer.Sound("sounds/slash.wav")
        self.slash_sound.set_volume(0.2)
        self.vegetable_group = pygame.sprite.Group()
        self.bomb_group = pygame.sprite.Group()
        self.timer = Timer(60)
        self.timer_thread = threading.Thread(target=self.timer.runTimer, daemon=True)
        self.score = Score()
        self.score_thread = threading.Thread(target=self.score.run_score, daemon=True)
        self.veg_gen = Generator(self.window, 'normal')
        self.veg_gen_thread = threading.Thread(target=self.veg_gen.run_generator, daemon=True)
        self.bomb_gen = BombGenerator(self.window, 'normal')
        self.bomb_gen_thread = threading.Thread(target=self.bomb_gen.run_generator, daemon=True)

    def start(self):
        self.window.resize((640, 480))
        self.start_threads()

        while not self.event_handler():
            self.window.draw_background()

            # Display timer
            timer_text = pygame.font.Font(None, 50).render("timer: {}".format(self.timer.game_time), True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(100, 50))
            self.window.screen.blit(timer_text, timer_rect)

            # Display score
            score_text = pygame.font.Font(None, 50).render("score: {}".format(self.score.total_score), True, (255, 255, 255))
            score_rect = timer_text.get_rect(center=(540, 50))
            self.window.screen.blit(score_text, score_rect)

            # Display vegetable
            self.vegetable_group.update(random.randint(1, 50) / 10, self.window.screen)
            self.vegetable_group.draw(self.window.screen)
            self.vegetable_group.add(self.veg_gen.get_vegetables())
            self.veg_gen.clear_vegetables()

            # Display Bomb
            self.bomb_group.update(random.randint(1, 50) / 10, self.window.screen)
            self.bomb_group.draw(self.window.screen)
            self.bomb_group.add(self.bomb_gen.get_bombs())
            self.bomb_gen.clear_bombs()

            self.clock.tick(60)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.timer.game_time == 0:
                pygame.quit()
                return True
            elif event.type == pygame.VIDEORESIZE:
                self.window.resize(event.size)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    for veg in self.vegetable_group:
                        if veg.rect.collidepoint(pygame.mouse.get_pos()):
                            self.slash_sound.play(0)
                            threading.Thread(target=self.score.add_point, daemon=True).start()
                            self.vegetable_group.remove(veg)
                            veg.kill()
                            if(self.score.total_score != 0 and self.score.total_score % 10 == 0):
                                self.timer.start_freeze_thread()
                    for bomb in self.bomb_group:
                        if bomb.rect.collidepoint(pygame.mouse.get_pos()):
                            self.slash_sound.play(0)
                            threading.Thread(target=self.score.divide_points, daemon=True).start()
                            self.bomb_group.remove(bomb)
                            bomb.kill()
        return False
    
    def start_threads(self):
        self.timer_thread.start()
        self.score_thread.start()
        self.veg_gen_thread.start()
        self.bomb_gen_thread.start()
