import random
from nif.control import get_control_digit


def generate():
    """Generates a random NIF number."""
    nif = str(random.randint(100000000, 999999999))
    return str(nif[:-1]) + get_control_digit(nif[:-1])
