import numpy as np
from math import log2
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


class Detector:
    def __init__(self, entropy):
        self._entropy = entropy

    def determine_encryption_in_percent(self, data):
        entropy, number_of_unique = self._entropy.calc_entropy(data, number_of_unique=True)
        # TODO  сколько делать 256? или ?
        return round(100 * entropy / log2(number_of_unique), 2)


class ShannonEntropy:
    def calc_entropy(self, data, number_of_unique=False):
        frequency = self._calc_frequency(data)
        result = 0
        for symbol in frequency.keys():
            freq = frequency[symbol]
            result -= freq * log2(freq)

        if number_of_unique:
            return result, len(frequency.keys())
        return result

    @staticmethod
    def _calc_frequency(data):
        unique, counts = np.unique(data, return_counts=True)
        data_length = len(data)
        return {unique[i]: counts[i] / data_length for i in range(len(unique))}
        # print(np.asarray((unique, counts)).T)


def read_file(path: str):
    with open(path, 'rb') as f:
        return f.read()


if __name__ == '__main__':
    detector = Detector(ShannonEntropy())
    text = list(read_file('file1'))
    entropies = []
    window_size = len(text) // 100
    hop = window_size // 7
    shift = 0
    limit = len(text)
    while shift + window_size < limit:
        window = text[shift:shift + window_size]
        entropies.append(detector.determine_encryption_in_percent(window))
        shift += hop

    x = np.linspace(window_size, len(text), len(entropies))
    y_smooth = savgol_filter(entropies, len(entropies) // 15, 5)
    avg_entropy = detector.determine_encryption_in_percent(text)
    y_avg = [avg_entropy] * len(x)

    plt.grid()
    plt.title('Оригинал')
    plt.xlabel(f'байты ({limit})', fontsize=12)
    plt.ylabel('энтропия %', fontsize=12)
    plt.plot(x, y_smooth, label=f'скользящее окно [{window_size}+{hop}]')
    plt.plot(x, y_avg, label=f'среднее = {avg_entropy}%')
    plt.legend()
    plt.show()
