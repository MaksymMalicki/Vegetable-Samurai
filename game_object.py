import random

import pygame
import math

gravity = 9.81


class GameObject(pygame.sprite.Sprite):

    def __init__(self, window_size, texture):
        super(GameObject, self).__init__()
        self.x_relative_y = 0
        self.image = pygame.transform.scale(pygame.image.load(texture), (100, 100))
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
        range = random.randint(self.pos_x, self.width) - self.pos_x if self.orientation == 1 else random.randint(1,
                                                                                                                 self.pos_x)
        self.theta = math.radians(random.randint(50, 80))
        self.initial_velocity = math.sqrt((range * gravity) / math.sin(2 * self.theta))
        self.initial_velocity = 1 if math.floor(self.initial_velocity) == 0 else self.initial_velocity

    def update(self, movement_shift=0.4, window=None):
        if not self.rect.colliderect(window.get_rect()):
            self.kill()
        self.pos_x += movement_shift * self.orientation
        self.x_relative_y += movement_shift
        self.pos_y = self.height - (self.x_relative_y * math.tan(self.theta) - (
                (gravity * self.x_relative_y ** 2) / (2 * self.initial_velocity ** 2 * math.cos(self.theta) ** 2)))
        self.rect.center = [self.pos_x, self.pos_y]