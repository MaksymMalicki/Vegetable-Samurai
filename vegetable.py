from game_object import GameObject
import random

textures = [
    "images/carrot.png",
]


class Vegetable(GameObject):

    def __init__(self, window_size):
        super().__init__(window_size=window_size, texture=random.choice(textures))
