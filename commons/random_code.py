import random
import string


def generate_random_code(size: int = 9):
    return "".join(random.choices(string.digits, k=size))
