import random


def generate_id(rooms):
    key = 1
    while key in rooms:
        key = random.randint(1, 1e18)
    return key
