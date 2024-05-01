import numpy as np
from math import log2

from src.main.app.settings.entropy_analyzer_settings import EntropyAnalyzerSettings


class EntropyCalculator:
    """
    Производит расчёт энтропии текста
    """

    def __init__(self):
        self._power = 256  # possible byte values (ASCII table power)

    def calc_entropy_in_percent(self, data: list[int]) -> float:
        """
        Рассчитывает энтропию текста в процентах

        :param data: текст в виде последовательности номеров байт

        :return: значение энтропии в процентах с двумя знаками после запятой
        """
        if len(data) == 0:
            return 0
        entropy, number_of_unique = self._calc_entropy(data)
        if number_of_unique > 1:
            return round(100 * entropy / log2(self._power), 2)
        return entropy

    def _calc_entropy(self, data: list[int]) -> (float, int):
        """
        Рассчитывает энтропию текста

        :param data: текст в виде последовательности номеров байт

        :return: значение энтропии и количество уникальных символов в тексте
        """
        frequency = self._calc_frequency(data)
        result = 0
        for symbol in frequency.keys():
            freq = frequency[symbol]
            result -= freq * log2(freq)
        return result, len(frequency)

    @staticmethod
    def _calc_frequency(data: list[int]) -> dict[int, float]:
        """
        Формирует словарь частотности символов

        :param data: текст в виде последовательности номеров байт

        :return: словарь частотности символов
        """
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

    def analyze(self, data: list[int]) -> float:
        """
        Вычисление энтропии текста в целом в процентах

        :param data: текст в виде последовательности номеров байт

        :return: энтропия текста в процентах с двумя знаками после запятой
        """
        return self._entropy_calculator.calc_entropy_in_percent(data)

    def window_analyze(self, data: list[int]) -> list[float]:
        """
        Вычисление энтропии текста методом "скользящего" окна

        :param data: текст в виде последовательности номеров байт

        :return: энтропия текста в процентах с двумя знаками после запятой
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
