from typing import Iterator, Union

import numpy as np
from math import log2

from src.main.app.model.settings.entropy_analyzer_settings import EntropyAnalyzerSettings


class EntropyCalculator:
    """
    Производит расчёт энтропии текста
    """

    def __init__(self):
        self._power = 256  # possible byte values (ASCII table power)

    def calc_entropy_in_percent_by_iter(self, data_iter: Iterator[list[int]]) -> float:
        return self._calc_entropy_in_percent(data_iter, self._calc_frequency_by_iter)

    def calc_entropy_in_percent(self, data: list[int]) -> float:
        return self._calc_entropy_in_percent(data, self._calc_frequency)

    def _calc_entropy_in_percent(self, data: Union[Iterator[list[int]], list[int]], calc_frequency_func) -> float:
        entropy, number_of_unique = self._calc_entropy(calc_frequency_func(data))
        if number_of_unique > 1:
            return round(100 * entropy / log2(self._power), 2)
        return entropy

    @staticmethod
    def _calc_entropy(frequency: dict[int, float]) -> (float, int):
        result = 0
        for symbol in frequency.keys():
            freq = frequency[symbol]
            result -= freq * log2(freq)
        return result, len(frequency)

    @staticmethod
    def _calc_frequency_by_iter(data_iter: Iterator[list[int]]) -> dict[int, float]:
        data_length = 0
        _dict_freq = dict()
        for data in data_iter:
            data_length += len(data)
            unique, counts = np.unique(data, return_counts=True)
            for i in range(len(unique)):
                uniq = unique[i]
                if uniq not in _dict_freq:
                    _dict_freq[uniq] = 0
                _dict_freq[uniq] += counts[i]
        return {uniq: _dict_freq[uniq] / data_length for uniq in _dict_freq} if data_length else dict()

    @staticmethod
    def _calc_frequency(data: list[int]) -> dict[int, float]:
        unique, counts = np.unique(data, return_counts=True)
        data_length = len(data)
        return {unique[i]: counts[i] / data_length for i in range(len(unique))}


class EntropyAnalyzer:
    """
    Рассчитывает энтропию текста (в целом и методом "скользящего" окна)
    """

    def __init__(self, entropy_calculator: EntropyCalculator, settings: EntropyAnalyzerSettings):
        self._entropy_calculator = entropy_calculator
        self._min_window_size = settings.min_window_size
        self._min_hope = settings.min_hope
        self._divider_for_window = settings.divider_for_window
        self._divider_for_hop = settings.divider_for_hop

    def analyze_by_iter(self, data_iter: Iterator[list[int]]) -> float:
        """
        Вычисление энтропии текста в целом в процентах
        """
        return self._entropy_calculator.calc_entropy_in_percent_by_iter(data_iter)

    def analyze(self, data: list[int]) -> float:
        """
        Вычисление энтропии текста в целом в процентах
        """
        return self._entropy_calculator.calc_entropy_in_percent(data)

    def window_analyze_by_iter(self, data_iter: Iterator[list[int]]) -> list[float]:
        """
        Вычисление энтропии текста методом "скользящего" окна
        """
        entropies = list()
        for data in data_iter:
            entropies.extend(self.window_analyze(data))
        return entropies

    def window_analyze(self, data: list[int]) -> list[float]:
        """
        Вычисление энтропии текста методом "скользящего" окна
        """
        window_size = self._calc_window_size(data)
        hop = self._calc_hop_size(window_size)
        shift = 0
        limit = len(data)
        entropies = []
        while shift + window_size <= limit:
            window = data[shift: shift + window_size]
            entropies.append(self.analyze(window))
            shift += hop
        return entropies

    def _calc_hop_size(self, window_size: int) -> int:
        """
        Вычисляет величину сдвига окна
        :param window_size: размер окна
        :return: величина сдвига
        """
        hop = window_size // self._divider_for_hop
        return max(hop, self._min_hope)

    def _calc_window_size(self, data: list[int]) -> int:
        """
        Вычисляет размер окна

        :param data: текст в виде последовательности номеров байт

        :return: размер окна
        """
        window_size = len(data) // self._divider_for_window
        return min(max(window_size, self._min_window_size), len(data))
