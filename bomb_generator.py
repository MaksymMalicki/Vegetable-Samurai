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
                cooldown = random.randint(3, 8)
                time.sleep(cooldown)
                with self.lock:
                    for _ in range(random.randint(1, 2)):
                        bomb = Bomb(self.window.screen.get_size())
                        print("new bomb")
                        self.bombs.append(bomb)
            elif self.mode != 'normal':
                cooldown = random.randint(1, 3)
                print(cooldown)
                time.sleep(cooldown)

    def get_bombs(self):
        with self.lock:
            return list(self.bombs)

    def clear_bombs(self):
        with self.lock:
            self.bombs.clear()

    def kill(self):
        raise SystemExit
