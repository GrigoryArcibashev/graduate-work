import numpy as np
from math import log2


class Entropy:
    def __init__(self):
        self._power = 256  # possible byte values (ASCII table power)

    def calc_entropy_in_percent(self, data):
        if len(data) == 0:
            return 0
        entropy, number_of_unique = self._calc_entropy(data, number_of_unique=True)
        if number_of_unique > 1:
            return round(100 * entropy / log2(self._power), 2)
        return entropy

    def _calc_entropy(self, data, number_of_unique=False):
        frequency = self._calc_frequency(data)
        result = 0
        for symbol in frequency.keys():
            freq = frequency[symbol]
            result -= freq * log2(freq)
        if number_of_unique:
            return result, len(frequency)
        return result

    @staticmethod
    def _calc_frequency(data):
        unique, counts = np.unique(data, return_counts=True)
        data_length = len(data)
        return {unique[i]: counts[i] / data_length for i in range(len(unique))}