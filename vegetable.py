import random

import pygame
import math

gravity = 9.81

textures = [
    "images/carrot.png",
]

class Vegetable(pygame.sprite.Sprite):

    def __init__(self, window_size):
        super(Vegetable, self).__init__()
        self.image = pygame.image.load(random.choice(textures))
        self.rect = self.image.get_rect()
        self.theta = 0
        self.width = window_size[0]
        self.height = window_size[1]
        self.pos_x = random.randint(self.width / 5, self.width * 4 / 5)
        self.pos_y = self.height
        self.orientation = random.choice([1, -1])
        self.initial_velocity = 0
        self.get_initial_v_and_theta()

    # TODO modify initial params to avoid creating objects with speeds which make it not possible to slice them
    # i.e. too low or to fast initial speed or very low angle of the object launch

    # TODO solve math error
    
    def get_initial_v_and_theta(self):
        # obliczamy kierunek wystrzału, losujemy kąt wystrzału, obliczamy prędkość początkową tak by warzywo
        # nie wystrzeliło poza ekran

        #do poprawienia
        range = random.randint(self.pos_x, self.width) - self.pos_x if self.orientation == 1 else random.randint(1, self.pos_x)
        self.theta = math.radians(random.randint(50, 80))
        self.initial_velocity = math.sqrt((range * gravity) / math.sin(2 * self.theta))
        self.x_relative_y = 0

    def update(self, movement_shift = 0.4, window = None):
        if not self.rect.colliderect(window.get_rect()):
            self.kill()
        self.pos_x += movement_shift * self.orientation
        
        # pozycja y musi być w funkcji czasu, ponieważ położenie x losujemy z zakresu 0 - width. Jeśli wylosujemy np.
        # 232, to położenie y mamy w chwili y(232) a nie y(0), dlatego to trzeba trackować osobno
        self.x_relative_y += movement_shift 
        self.pos_y = self.height - (self.x_relative_y * math.tan(self.theta) - (
                (gravity * self.x_relative_y ** 2) / (2 * self.initial_velocity ** 2 * math.cos(self.theta) ** 2)))
        self.rect.center = [self.pos_x, self.pos_y]
