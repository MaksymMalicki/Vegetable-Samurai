import time
import threading

class Timer:

    def __init__(self, game_time=60):
        self.lock = threading.Lock()
        self.game_time = game_time
        self.freeze_time = 10

    def run_timer(self):
        while True:
            with self.lock:
                self.game_time -= 1
            time.sleep(1)

    def freeze_timer(self):
        with self.lock:
            time.sleep(self.freeze_time)

    def start_freeze_thread(self):
        threading.Thread(target=self.freeze_timer, daemon=True).start()
