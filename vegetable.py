"""
Class Vegetable extends from class GameObject. It instantiates the vegetable object,
that appears on the screen.
"""

import random
from game_object import GameObject

textures = [
    "images/carrot.png", "images/potato.webp", "images/beetroot.webp", "images/watermelon.webp"
]


class Vegetable(GameObject):
    """
    Class Bomb:
    attributes:
        none
    methods:
        contructor: inherits from GameObject and adds two atributes - window_size and texture
    """
    def __init__(self, window_size):
        super().__init__(window_size=window_size, texture=random.choice(textures))
