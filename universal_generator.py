import time
import random
import threading


class UniversalGenerator:
    def __init__(self, window, gen_object, time_range=(0.5, 4.0), objects_range=(1, 3)):
        self.window = window
        self.gen_object = gen_object
        self.object_list = []
        self.lock = threading.Lock()
        self.time_range = time_range
        self.objects_range = objects_range

    def run_generator(self):
        while True:
            time.sleep(random.uniform(*self.time_range))
            with self.lock:
                for _ in range(random.randint(*self.objects_range)):
                    generated_object = self.gen_object(self.window.screen.get_size())
                    self.object_list.append(generated_object)

    def get_objects(self):
        with self.lock:
            return list(self.object_list)

    def clear_objects(self):
        with self.lock:
            self.object_list.clear()
