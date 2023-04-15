import random

import pygame
import math

gravity = 9.81


class Vegetable(pygame.sprite.Sprite):

    def __init__(self, window_size):
        super(Vegetable, self).__init__()
        self.image = pygame.image.load("carrot.png")
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
        self.orientation = random.choice([1, -1])
        self.pos_x = random.randint(0, self.width)
        self.pos_y = self.height
        range = random.randint(self.pos_x, self.width) if self.orientation == 1 else random.randint(0, self.pos_x)
        self.theta = math.radians(random.randint(45, 60))
        self.initial_velocity = math.sqrt((range * gravity) / math.sin(2 * self.theta))
        print(self.orientation, self.pos_x, self.pos_y, range, self.theta, self.initial_velocity)

    def suicide(self):
        self.kill()

    def update(self, dt=0.4, window=None):
        if not self.rect.colliderect(window.get_rect()):
            print("samobój")
            self.suicide()
        self.pos_x += dt * self.orientation
        self.pos_y = self.height - (self.pos_x * math.tan(self.theta) - (
                (gravity * self.pos_x ** 2) / (2 * self.initial_velocity ** 2 * math.cos(self.theta) ** 2)))
        self.rect.center = [self.pos_x, self.pos_y]
