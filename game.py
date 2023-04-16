import threading
import pygame
from window import Window
from vegetable import Vegetable
from timer import Timer

class Game:

    def __init__(self):
        pygame.init()
        self.window = Window(640, 480)
        self.clock = pygame.time.Clock()
        self.vegetable = Vegetable(self.window.screen.get_size())
        self.vegetable_group = pygame.sprite.Group()
        self.vegetable_group.add(self.vegetable)
        self.timer = Timer(0)
        self.timer_thread = threading.Thread(target=self.timer.runTimer)

    def start(self):
        self.window.resize((640, 480))
        self.timer_thread.start()
        while not self.event_handler():
            self.window.draw_background()
            timer_text = pygame.font.Font(None, 50).render("{}".format(self.timer.game_time), True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(50, 50))
            self.window.screen.blit(timer_text, timer_rect)
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
                self.timer_thread.join()
                pygame.quit()

                return True
            elif event.type == pygame.VIDEORESIZE:
                self.window.resize(event.size)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if self.vegetable.rect.collidepoint(pygame.mouse.get_pos()):
                        print("pociachano tej")
                        self.vegetable.suicide()
        return False
