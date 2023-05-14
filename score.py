import time
import threading

# TODO mutex while cutting different objects

class Score:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_score = 0

    def add_point(self):
        with self.lock:
            self.total_score += 1

    def remove_point(self):
        with self.lock:
            self.total_score -= 1

    def run_score(self):
        while True:
            time.sleep(1)
        
    def kill(self):
        raise SystemExit