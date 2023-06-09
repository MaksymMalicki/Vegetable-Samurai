"""
timer.py

This module contains the Timer class, which represents a game timer.
"""
import threading
import time

class Timer:
    """
    The Timer class represents a game timer.

    Attributes:
        lock (threading.Lock): A lock object used for thread synchronization.
        game_time (int): The initial game time in seconds.
        freeze_time (int): The duration of the freeze time in seconds.

    Methods:
        run_timer: Starts the timer in a separate thread.
        freeze_timer: Freezes the timer for a specific duration.
        start_freeze_thread: Starts the freeze timer in a separate thread.
    """

    def __init__(self, game_time=60):
        """
        Initializes a Timer instance.

        Args:
            game_time (int, optional): The initial game time in seconds. Defaults to 60.
        """
        self.lock = threading.Lock()
        self.game_time = game_time
        self.freeze_time = 10

    def run_timer(self):
        """
        Starts the timer in a separate thread.
        """
        while True:
            with self.lock:
                self.game_time -= 1
            time.sleep(1)

    def freeze_timer(self):
        """
        Freezes the timer for a specific duration.
        """
        with self.lock:
            time.sleep(self.freeze_time)

    def start_freeze_thread(self):
        """
        Starts the freeze timer in a separate thread.
        """
        threading.Thread(target=self.freeze_timer, daemon=True).start()
