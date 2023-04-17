import threading
import pygame
import time
from window import Window
from score import Score
from vegetable import Vegetable
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
        self.slash_sound = pygame.mixer.Sound("sounds/slash.wav")
        #pygame.mixer.Channel(0).play(pygame.mixer.Sound("Naruto - Fight.mp3"))
        self.vegetable_group = pygame.sprite.Group()
        self.vegetable_group.add(self.vegetable)
        self.timer = Timer(0)
        self.timer_thread = threading.Thread(target=self.timer.runTimer)
        self.timer_thread.daemon = True
        self.score = Score()
        self.score_thread = threading.Thread(target=self.score.run_score)
        self.score_thread.daemon = True

    def start(self):
        self.window.resize((640, 480))
        self.timer_thread.start()
        self.score_thread.start()
        while not self.event_handler():
            self.window.draw_background()
            timer_text = pygame.font.Font(None, 50).render("timer: {}".format(self.timer.game_time), True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(100, 50))
            self.window.screen.blit(timer_text, timer_rect)
            score_text = pygame.font.Font(None, 50).render("score: {}".format(self.score.total_score), True, (255, 255, 255))
            score_rect = timer_text.get_rect(center=(540, 50))
            self.window.screen.blit(score_text, score_rect)
            self.vegetable_group.draw(self.window.screen)
            self.vegetable_group.update(self.clock.tick(60), self.window.screen)
            if not self.vegetable_group.has(self.vegetable):
                print("nowy ziomek!")
                self.vegetable = Vegetable(self.window.screen.get_size())
                self.vegetable_group.add(self.vegetable)
            self.clock.tick(60)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for thread in threading.enumerate(): 
                    print(thread.name)
                self.timer.kill()
                self.score.kill()
                pygame.quit()

                return True
            elif event.type == pygame.VIDEORESIZE:
                self.window.resize(event.size)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if self.vegetable.rect.collidepoint(pygame.mouse.get_pos()):
                        self.slash_sound.play(0)
                        self.score.add_point()
                        print(f'wynik: {self.score.total_score}')
                        print("pociachano tej")
                        self.vegetable.kill()
        return False
