import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from src.main.app.encryption.encryption_filter import EncryptionFilter
from src.main.app.words_service.word_loader import SimpleWordLoader
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.encryption.encryption_determinator import EncryptionDeterminatorByEntropy, EncryptionDeterminatorByHEX
from src.main.app.encryption.entropy.entropy import Entropy
from src.main.app.encryption.entropy.entropy_analyzer import EntropyAnalyzer
from src.main.app.file_reader import read_file


def plot_entropy(title, entropies, hop, window_size, limit):
    x = np.linspace(window_size, limit, len(entropies))
    params = _get_savgol_filter_params(len(entropies))
    y_smooth = savgol_filter(entropies, params[0], params[1]) if params else entropies
    description = f'скользящее окно [{window_size}+{hop}] * {len(entropies)}'
    if params:
        description += f'\nws/order = {params[0]}/{params[1]}'

    figure = plt.figure()
    figure.set(xlabel=f'байты', ylabel='энтропия %', title=title, fontsize=12)
    # figure.plot(x, y_smooth, label=description)
    figure.legend()
    ax = figure.gca()
    ax.grid()
    ax.plot(x, y_smooth, label=description)
    ax.show()


def _get_savgol_filter_params(entropies_len: int):
    order = 3
    size = 20
    while size >= entropies_len and size > order:
        size /= 2
    if order < size < entropies_len:
        return size, order
    return None


def main():
    matplotlib.use('TkAgg')
    text = read_file(f'../../../source/x.txt')
    # text = input().encode()
    data = list(text)
    len_before = len(data)

    ed = EncryptionDeterminatorByEntropy(EntropyAnalyzer(Entropy()))
    ed_hex = EncryptionDeterminatorByHEX()
    ef = EncryptionFilter(WordDictService(SimpleWordLoader('../../words_service/words_by_len.bin')))
    data = ef.filter(data)
    is_encr, entropy, entropy_above_border = ed.determinate(data)
    is_hex = ed_hex.determinate(text)

    cut_out = round(100 - len(data) / (len_before / 100), 2)
    print(f'\nВырезано {cut_out}%')
    print(f'{is_encr}\n{entropy}% | {entropy_above_border}%')
    if is_hex:
        print('!Обнаружен HEX!')

    # entropy_analyzer = EntropyAnalyzer(Entropy())
    # entropies, window_size, hop = entropy_analyzer.window_analyze(data)
    #
    # title = f'{f"ЕСТЬ ШИФР (entr={is_encr}) (hex={is_hex})" if is_encr or is_hex else "НЕТ ШИФРА"}, вырезано {cut_out}%'
    # title += f'\nЭнтропия {entropy}% | {entropy_above_border}%{",  => HEX!" if is_hex else ""}'
    # plot_entropy(title, entropies, hop, window_size, len(data))


if __name__ == '__main__':
    main()
