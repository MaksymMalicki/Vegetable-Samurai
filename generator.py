import time
import random

class Generator:
    def __init__(self, mode='normal'):
        self.mode = mode
        pass

    # TODO remove print statements after done with debug
    def run_generator(self):
        while True:
            if self.mode == 'normal':
                print(cooldown)
                time.sleep(random.randint(1,10))
            elif self.mode != 'normal':
                cooldown = random.randint(1,3)
                print(cooldown)
                time.sleep(cooldown)
            

    def kill():
        raise SystemExit