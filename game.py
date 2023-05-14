import threading
import pygame
import time
import random
from window import Window
from score import Score
from vegetable import Vegetable
from generator import Generator
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
        pygame.mixer.music.set_volume(0.4)
        self.slash_sound = pygame.mixer.Sound("sounds/slash.wav")
        self.slash_sound.set_volume(0.2)
        self.vegetable_group = pygame.sprite.Group()
        self.vegetable_group.add(self.vegetable)
        self.timer = Timer(0)
        self.timer_thread = threading.Thread(target=self.timer.runTimer)
        self.timer_thread.daemon = True
        self.score = Score()
        self.score_thread = threading.Thread(target=self.score.run_score)
        self.score_thread.daemon = True
        self.gen = Generator(self.window,'normal')
        self.gen_thread = threading.Thread(target=self.gen.run_generator)
        self.gen_thread.daemon = True
        self.bomb_group = None

    def add_vegetables(self, count):
        for _ in range(count):
            vegetable = Vegetable(self.window.screen.get_size())
            self.vegetable_group.add(vegetable)

    def start(self):
        self.window.resize((640, 480))
        self.timer_thread.start()
        self.score_thread.start()
        self.gen_thread.start()
        while not self.event_handler():
            self.window.draw_background()
            timer_text = pygame.font.Font(None, 50).render("timer: {}".format(self.timer.game_time), True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(100, 50))
            self.window.screen.blit(timer_text, timer_rect)
            score_text = pygame.font.Font(None, 50).render("score: {}".format(self.score.total_score), True, (255, 255, 255))
            score_rect = timer_text.get_rect(center=(540, 50))
            self.window.screen.blit(score_text, score_rect)

            # TODO move to thread

            self.vegetable_group.update(random.randint(1, 50) / 10, self.window.screen)
            self.vegetable_group.draw(self.window.screen)
            
            
            self.vegetable_group.add(self.gen.get_vegetables())
            self.gen.clear_vegetables()
            self.clock.tick(60)

    # TODO remove print statement
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for thread in threading.enumerate(): 
                    print(thread.name)
                self.timer.kill()
                self.score.kill()
                self.gen.kill()
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
                            threading.Thread(target=self.timer.freeze_timer, daemon=True).start()
                    # for bomb in self.bomb_group:
                    #     threading.Thread(target=self.score.remove_point, daemon=True)
                    #     pass
        return False
