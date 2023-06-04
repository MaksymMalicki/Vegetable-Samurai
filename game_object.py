import random
import pygame
import math

gravity = 3.81

class GameObject(pygame.sprite.Sprite):

    def __init__(self, window_size, texture):
        super(GameObject, self).__init__()
        self.x_relative_y = 0
        self.image = pygame.transform.scale(pygame.image.load(texture), (75, 75))
        self.rect = self.image.get_rect()
        self.theta = 0
        self.width = window_size[0]
        self.height = window_size[1]
        # TODO modify
        self.orientation = random.choice([1, -1])
        self.pos_x = random.randint(int(self.width / 10), int(self.width * 2 / 3)) if self.orientation else random.randint(int(self.width * 2 / 5), int(self.width * 9 / 10))
        self.pos_y = self.height
        self.ini_vel = 0
        self.get_initial_v_and_theta()

    # TODO modify initial params to avoid creating objects with speeds which make it not possible to slice them
    # i.e. too low or to fast initial speed or very low angle of the object launch

    def get_initial_v_and_theta(self):
        range = random.randint(self.pos_x, self.width) - self.pos_x if self.orientation == 1 else random.randint(1,self.pos_x)
        self.theta = math.radians(random.randint(65, 80))
        self.ini_vel = math.sqrt((range * gravity) / math.sin(2 * self.theta))
        self.ini_vel = random.randint(40,55) if math.floor(self.ini_vel) < 40 else self.ini_vel
        self.ini_vel = random.randint(55,70) if math.floor(self.ini_vel) > 70 else self.ini_vel
        self.ini_vel = 50
        print(self.ini_vel)
        
    def update(self, movement_shift=0.2, window=None):
        if not self.rect.colliderect(window.get_rect()):
            self.kill()
        self.pos_x += movement_shift * self.orientation
        self.x_relative_y += movement_shift
        self.pos_y = self.height - (self.x_relative_y * math.tan(self.theta) - ((gravity * self.x_relative_y ** 2) / (2 * self.ini_vel ** 2 * math.cos(self.theta) ** 2)))
        self.rect.center = [self.pos_x, self.pos_y]
