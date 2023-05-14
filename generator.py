import time
import random
import threading
from vegetable import Vegetable


class Generator:
    def __init__(self,window, mode='normal'):
        self.mode = mode
        self.window = window
        self.lock = threading.Lock()
        self.vegetables = []

    # TODO remove print statements after done with debug
    def run_generator(self):
        while True:
            if self.mode == 'normal':
                cooldown = random.randint(1,3)
                print(cooldown)
                time.sleep(cooldown)
                with self.lock:
                    for _ in range(random.randint(1,3)):
                        vegetable = Vegetable(self.window.screen.get_size())
                        self.vegetables.append(vegetable)
            elif self.mode != 'normal':
                cooldown = random.randint(1,3)
                print(cooldown)
                time.sleep(cooldown)

    def get_vegetables(self):
        with self.lock:
            return list(self.vegetables)
    
    def clear_vegetables(self):
        with self.lock:
            self.vegetables.clear()
        
            

    def kill():
        raise SystemExit