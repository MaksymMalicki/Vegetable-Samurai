import random

import pygame
from window import Window
from vegetable import Vegetable


class Game:

    def __init__(self):
        pygame.init()
        self.window = Window(640, 480)
        self.clock = pygame.time.Clock()
        self.vegetable = Vegetable(self.window.screen.get_size())
        self.vegetable_group = pygame.sprite.Group()
        self.vegetable_group.add(self.vegetable)

    def start(self):
        self.window.resize((640, 480))
        while not self.event_handler():
            self.window.draw_background()

            self.vegetable_group.draw(self.window.screen)
            self.vegetable_group.update(0.5, self.window.screen)
            if not self.vegetable_group.has(self.vegetable):
                print("nowy ziomek!")
                self.vegetable = Vegetable(self.window.screen.get_size())
                self.vegetable_group.add(self.vegetable)

            self.clock.tick(60)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
