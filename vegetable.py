import random

import pygame
import math

gravity = 9.81


class Vegetable(pygame.sprite.Sprite):

    def __init__(self, window_size):
        super(Vegetable, self).__init__()
        self.image = pygame.image.load("images/carrot.png")
        self.rect = self.image.get_rect()
        self.theta = 0
        self.orientation = 1
        self.width = window_size[0]
        self.height = window_size[1]
        self.pos_x = 0
        self.pos_y = 0
        self.initial_velocity = 0
        self.get_initial_v_and_theta()

    def get_initial_v_and_theta(self):
        self.pos_x = random.randint(1, self.width)
        self.pos_y = self.height
        # obliczamy kierunek wystrzału, losujemy kąt wystrzału, obliczamy prędkość początkową tak by warzywo
        # nie wystrzeliło poza ekran
        self.orientation = random.choice([1, -1])
        range = random.randint(self.pos_x, self.width) if self.orientation == 1 else random.randint(1, self.pos_x)
        self.theta = math.radians(random.randint(45, 60))
        self.initial_velocity = math.sqrt((range * gravity) / math.sin(2 * self.theta))
        self.time = 0

    def suicide(self):
        self.kill()

    def update(self, dt = 0.4, window = None):
        if not self.rect.colliderect(window.get_rect()):
            self.suicide()
        #print(self.orientation)
        self.pos_x += dt * self.orientation
        # pozycja y musi być w funkcji czasu, ponieważ położenie x losujemy z zakresu 0 - width. Jeśli wylosujemy np.
        # 232, to położenie y mamy w chwili y(232) a nie y(0), dlatego to trzeba trackować osobno
        self.time += dt * self.orientation
        self.pos_y = self.height - (self.time * math.tan(self.theta) - (
                (gravity * self.time ** 2) / (2 * self.initial_velocity ** 2 * math.cos(self.theta) ** 2)))
        #print(self.pos_x, self.pos_y)
        self.rect.center = [self.pos_x, self.pos_y]
