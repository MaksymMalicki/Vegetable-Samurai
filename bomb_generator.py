import time
import random
import threading
from bomb import Bomb


class BombGenerator:
    def __init__(self, window, mode='normal'):
        self.mode = mode
        self.window = window
        self.lock = threading.Lock()
        self.bombs = []

    # TODO remove print statements after done with debug
    def run_generator(self):
        while True:
            if self.mode == 'normal':
                time.sleep(random.randint(3, 8))
                with self.lock:
                    for _ in range(random.randint(1, 2)):
                        bomb = Bomb(self.window.screen.get_size())
                        self.bombs.append(bomb)
            elif self.mode == 'hard':
                time.sleep(random.randint(1, 3))

    def get_bombs(self):
        with self.lock:
            return list(self.bombs)

    def clear_bombs(self):
        with self.lock:
            self.bombs.clear()