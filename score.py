"""
score.py

This module contains the Score class which represents game score.
"""
import time
import threading

class Score:
    """
    The Score class represents the game score.

    Attributes:
        lock (threading.Lock): A lock object used for thread synchronization.
        total_score (int): The total score.

    Methods:
        add_point: Adds a point to the score.
        divide_points: Divides the total score by 2.
        run_score: Starts the score update loop in a separate thread.
    """

    def __init__(self):
        """
        Initializes a Score instance.
        """
        self.lock = threading.Lock()
        self.total_score = 0

    def add_point(self):
        """
        Adds a point to the score.
        """
        with self.lock:
            self.total_score += 1

    def divide_points(self):
        """
        Divides the total score by 2.
        """
        with self.lock:
            self.total_score //= 2

    def run_score(self):
        """
        Starts the score update loop in a separate thread.
        """
        while True:
            time.sleep(1)
