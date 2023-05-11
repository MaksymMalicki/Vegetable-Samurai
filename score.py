import time

# TODO mutex while cutting 2 objects

class Score:
    def __init__(self):
        self.total_score = 0

    def add_point(self):
        self.total_score += 1

    def run_score(self):
        while True:
            time.sleep(1)
        
    def kill(self):
        raise SystemExit