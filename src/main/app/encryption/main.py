import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from src.main.app.encryption.entropy import Entropy
from src.main.app.encryption.entropy_analyzer import EntropyAnalyzer
from src.main.app.encryption.file_reader import read_file


def plot_entropy(title, entropy, entropies, hop, window_size, limit):
    x = np.linspace(window_size, limit, len(entropies))
    y_smooth = entropies  # savgol_filter(entropies, len(entropies) // 15, 0)
    avg_entropy = entropy
    y_avg = [avg_entropy] * len(x)
    plt.grid()
    plt.title(title)
    plt.xlabel(f'байты', fontsize=12)
    plt.ylabel('энтропия %', fontsize=12)
    plt.plot(x, y_smooth, label=f'скользящее окно [{window_size}+{hop}]')
    plt.plot(x, y_avg, label=f'среднее = {avg_entropy}%')
    plt.legend()
    plt.show()


def main():
    data = list(read_file('../../source/orig/2'))

    entropy_analyzer = EntropyAnalyzer(Entropy())
    entropies, window_size, hop = entropy_analyzer.window_analyze(data)

    entropy = entropy_analyzer.analyze(data)
    print(np.mean(entropies))
    title = 'Шифр'
    plot_entropy(title, entropy, entropies, hop, window_size, len(data))


if __name__ == '__main__':
    main()
