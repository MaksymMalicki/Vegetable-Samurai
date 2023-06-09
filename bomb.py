"""
Class Bomb extends from class GameObject. It instantiates the bomb object,
that appears on the screen.
"""

from game_object import GameObject


class Bomb(GameObject):
    """
    Class Bomb:
    attributes:
        brak
    methods:
        contructor: inherits from GameObject and adds two atributes - window_size and texture
    """

    def __init__(self, window_size):
        super().__init__(window_size=window_size, texture="images/bomb.webp")
