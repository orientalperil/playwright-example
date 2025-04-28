import random
import time


def human_type(element, text):
    for char in text:
        element.type(char, delay=random.randint(100, 300))


def random_delay(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))
