import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from src.main.app.encryption.encr_filter.encryption_filter import EncryptionFilter
from src.main.app.encryption.encr_filter.words.word_loader import SimpleWordLoader
from src.main.app.encryption.encr_filter.words.word_provider import WordProvider
from src.main.app.encryption.encryption_determinator import EncryptionDeterminator
from src.main.app.encryption.entropy.entropy import Entropy
from src.main.app.encryption.entropy.entropy_analyzer import EntropyAnalyzer
from src.main.app.file_reader import read_file


def plot_entropy(title, entropies, hop, window_size, limit):
    x = np.linspace(window_size, limit, len(entropies))
    params = _get_savgol_filter_params(len(entropies))
    y_smooth = savgol_filter(entropies, params[0], params[1]) if params else entropies
    plt.grid()
    plt.title(title)
    plt.xlabel(f'байты', fontsize=12)
    plt.ylabel('энтропия %', fontsize=12)
    description = f'скользящее окно [{window_size}+{hop}] * {len(entropies)}'
    if params:
        description += f'\nws/order = {params[0]}/{params[1]}'
    plt.plot(x, y_smooth, label=description)
    plt.legend()
    plt.show()


def _get_savgol_filter_params(entropies_len: int):
    order = 3
    size = 20
    while size >= entropies_len and size > order:
        size /= 2
    if order < size < entropies_len:
        return size, order
    return None


def main():
    filename = 'x'
    data = list(read_file(f'../../../source/{filename}.txt'))
    # data = list(map(ord, input()))
    len_before = len(data)

    ed = EncryptionDeterminator(EntropyAnalyzer(Entropy()))
    ef = EncryptionFilter(WordProvider(SimpleWordLoader('../encr_filter/words/words.txt')))
    data = ef.filter(data)
    is_encr, entropy, entropy_above_border = ed.determinate(data)

    cut_out = round(100 - len(data) / (len_before / 100), 2)
    print(f'\nВырезано {cut_out}%')
    print(f'{is_encr}\n{entropy}% | {entropy_above_border}%')

    entropy_analyzer = EntropyAnalyzer(Entropy())
    entropies, window_size, hop = entropy_analyzer.window_analyze(data)

    title = f'{"ЕСТЬ ШИФР" if is_encr else "НЕТ ШИФРА"}, вырезано {cut_out}%'
    title += f'\nЭнтропия {entropy}% | {entropy_above_border}%'
    plot_entropy(title, entropies, hop, window_size, len(data))


if __name__ == '__main__':
    main()
