import numpy as np
from math import log2


class EntropyCalculator:
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


class EntropyAnalyzer:
    def __init__(self, entropy_calculator: EntropyCalculator):
        self._entropy_calculator = entropy_calculator
        self._min_window_size = 100
        self._min_hope = 1
        self._divider_for_window = 120
        self._divider_for_hop = 5

    def analyze(self, data):
        return self._entropy_calculator.calc_entropy_in_percent(data)

    def window_analyze(self, data):
        window_size = self._calc_window_size(data)
        hop = self._calc_hop_size(window_size)
        shift = 0
        limit = len(data)
        entropies = []
        while shift + window_size <= limit:
            window = data[shift: shift + window_size]
            entropies.append(self.analyze(window))
            shift += hop
        return entropies, window_size, hop

    def _calc_hop_size(self, window_size):
        hop = window_size // self._divider_for_hop
        return max(hop, self._min_hope)

    def _calc_window_size(self, data):
        window_size = len(data) // self._divider_for_window
        return min(max(window_size, self._min_window_size), len(data))
