from game_object import GameObject

class Bomb(GameObject):
    def __init__(self, window_size):
        super().__init__(window_size=window_size, texture="images/bomb.webp")
