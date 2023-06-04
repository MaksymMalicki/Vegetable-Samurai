from game_object import GameObject
import random

textures = [
    "images/carrot.png","images/potato.webp","images/beetroot.webp","images/watermelon.webp"
]


class Vegetable(GameObject):

    def __init__(self, window_size):
        super().__init__(window_size=window_size, texture=random.choice(textures))
