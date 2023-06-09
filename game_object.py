import random
import math
import pygame

GRAVITY = 9.81


class GameObject(pygame.sprite.Sprite):

    def __init__(self, window_size, texture):
        super(GameObject, self).__init__()
        self.x_relative_y = 0
        self.image = pygame.transform.scale(pygame.image.load(texture), (75, 75))
        self.rect = self.image.get_rect()
        self.theta = 0
        self.width = window_size[0]
        self.height = window_size[1]
        self.orientation = random.choice([1, -1])
        self.pos_x = random.randint(self.width / 10, self.width * 3 / 5) \
            if self.orientation == 1 else random.randint(self.width * 2 / 5, self.width * 9 / 10)
        self.pos_y = self.height
        self.ini_vel = 0
        self.get_initial_v_and_theta()
        self.time = 0
        self.time_step = 0.1

    def get_initial_v_and_theta(self):
        """
        This method is responsible for getting the initial params for the parabolic movement
        :return:
        """
        shoot_range = random.randint(self.pos_x, self.width) - self.pos_x \
            if self.orientation == 1 else random.randint(1, self.pos_x)
        self.theta = math.radians(random.randint(65, 80))
        self.ini_vel = math.sqrt((shoot_range * GRAVITY) / math.sin(2 * self.theta))
        self.ini_vel = random.randint(70, 100)

    def update(self, movement_shift=0.001, window=None):
        """
        This method updates the coordinates of the center of the object
        :param movement_shift:
        :param window:
        :return:
        """
        if not self.rect.colliderect(window.get_rect()):
            self.kill()
        self.pos_x += movement_shift * self.orientation
        self.x_relative_y += movement_shift
        self.pos_y = self.height - (self.x_relative_y * math.tan(self.theta)
                                    - ((GRAVITY * self.x_relative_y ** 2)
                                    / (2 * self.ini_vel ** 2 * math.cos(self.theta) ** 2)))
        self.rect.center = [self.pos_x, self.pos_y]
