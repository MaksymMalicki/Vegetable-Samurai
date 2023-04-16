import time


class Timer:
    def __init__(self, game_time=0):
        self.game_time = game_time

    def runTimer(self):
        while True:
            self.game_time += 1
            time.sleep(1)