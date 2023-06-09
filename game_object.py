"""
game_object.py

This module contains the GameObject class, which represents a game object in the game.
It provides methods for updating the object's position.
"""

import random
import math
import pygame

GRAVITY = 9.81


class GameObject(pygame.sprite.Sprite):
    """
    The GameObject class represents a game object in the game.
    It provides methods for updating the object's position and drawing it on the screen.
    """

    def __init__(self, window_size, texture):
        super().__init__()
        self.x_relative_y = 0
        self.image = pygame.transform.scale(pygame.image.load(texture), (75, 75))
        self.rect = self.image.get_rect()
        self.theta = math.radians(random.randint(65, 80))
        self.win_size = window_size
        self.position = self.get_position()
        self.ini_vel = random.randint(70, 100)

    def get_position(self):
        """
        This method is responsible for getting the initial position of the parabolic movement
        
        Parameters:
            none
        Returns:
            tuple: contains starting x and starting y position and launch direction of an object
        """
        launch_direction = random.choice([1, -1])
        if launch_direction == 1:
            return random.randint(self.win_size[1] / 10, self.win_size[0] * 3 / 5), \
                self.win_size[1], launch_direction
        return random.randint(self.win_size[1] * 2 / 5, self.win_size[0] * 9 / 10), \
            self.win_size[1], launch_direction

    def update(self, movement_shift=0.001, window=None):
        """
        This method updates the coordinates of the center of the object

        Parameters:
            movement_shift : float : indicates how far the object can move in each clock tick
            window: Window : object of a Window class on which we display our objects
        """
        if not self.rect.colliderect(window.get_rect()):
            self.kill()
        pos_x, pos_y, choice = self.position
        pos_x += movement_shift * choice
        self.x_relative_y += movement_shift
        pos_y = self.win_size[1] - (self.x_relative_y * math.tan(self.theta)
                                    - ((GRAVITY * self.x_relative_y ** 2)
                                    / (2 * self.ini_vel ** 2 * math.cos(self.theta) ** 2)))
        self.rect.center = [pos_x, pos_y]
        self.position = pos_x, pos_y, choice
