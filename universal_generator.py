"""
universal_generator.py

This module contains the UniversalGenerator class, which handles the generation of objects.
"""
import time
import random
import threading


class UniversalGenerator:
    """
    UniversalGenerator class handles the generation of objects in the game.

    Attributes:
        window (object): The game window.
        gen_object (class): The class representing the generated objects.
        time_range (tuple): The range of time between object generation in seconds.
        objects_range (tuple): The range of the number of objects generated at a time.

    Methods:
        run_generator: Starts the generator in a separate thread.
        get_objects: Returns a list of the generated objects.
        clear_objects: Clears the list of generated objects.
    """

    def __init__(self, window, gen_object, time_range=(0.5, 4.0), objects_range=(1, 3)):
        self.window = window
        self.gen_object = gen_object
        self.object_list = []
        self.lock = threading.Lock()
        self.time_range = time_range
        self.objects_range = objects_range

    def run_generator(self):
        """
        Starts the generator in a separate thread.
        """
        while True:
            time.sleep(random.uniform(*self.time_range))
            with self.lock:
                for _ in range(random.randint(*self.objects_range)):
                    generated_object = self.gen_object(self.window.screen.get_size())
                    self.object_list.append(generated_object)

    def get_objects(self):
        """
        Returns a list of the generated objects.

        Returns:
            list: A list of the generated objects.
        """
        with self.lock:
            return list(self.object_list)

    def clear_objects(self):
        """
        Clears the list of generated objects.
        """
        with self.lock:
            self.object_list.clear()
