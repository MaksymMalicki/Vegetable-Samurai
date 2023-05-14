import time
import threading

class Score:

    def __init__(self):
        self.lock = threading.Lock()
        self.total_score = 0
        
    def add_point(self):
        with self.lock:
            self.total_score += 1

    def divide_points(self):
        with self.lock:
            self.total_score //= 2

    def run_score(self):
        while True:
            time.sleep(1)