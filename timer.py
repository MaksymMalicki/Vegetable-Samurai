import time
import threading


class Timer:
    def __init__(self, game_time=0):
        self.lock = threading.Lock()
        self.game_time = game_time
        self.freeze_time = 10

    def runTimer(self):
        while True:
            with self.lock:
                self.game_time += 1
            time.sleep(1)

    def kill(self):
        raise SystemExit

    def freeze_timer(self):
        with self.lock:
            time.sleep(self.freeze_time)
