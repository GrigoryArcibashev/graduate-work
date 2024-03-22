import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from src.main.app.encryption.entropy.entropy import Entropy
from src.main.app.encryption.entropy.entropy_analyzer import EntropyAnalyzer
from src.main.app.file_reader import read_file


def plot_entropy(title, entropy, entropies, hop, window_size, limit):
    x = np.linspace(window_size, limit, len(entropies))
    y_smooth = savgol_filter(entropies, 10, 3)
    avg_entropy = entropy
    y_avg = [avg_entropy] * len(x)
    plt.grid()
    plt.title(title)
    plt.xlabel(f'байты', fontsize=12)
    plt.ylabel('энтропия %', fontsize=12)
    plt.plot(x, y_smooth, label=f'скользящее окно [{window_size}+{hop}] * {len(entropies)}')
    plt.plot(x, y_avg, label=f'среднее = {avg_entropy}%')
    plt.legend()
    plt.show()


def main():
    folder = 'encr'
    filename = 12#input()
    data = list(read_file(f'../../../source/{folder}/{filename}.txt'))

    entropy_analyzer = EntropyAnalyzer(Entropy())
    entropies, window_size, hop = entropy_analyzer.window_analyze(data)

    entropy = entropy_analyzer.analyze(data)
    title = f'{folder}/{filename}'
    plot_entropy(title, entropy, entropies, hop, window_size, len(data))


if __name__ == '__main__':
    main()
