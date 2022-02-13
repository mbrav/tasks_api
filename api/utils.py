from random import randint


class Random:
    """Utility class for Random number generation"""

    @staticmethod
    def rand_int():
        return randint(0, 4294967296)
