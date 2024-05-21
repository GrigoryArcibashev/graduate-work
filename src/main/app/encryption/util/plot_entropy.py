import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from src.main.app.encryption.encryption_determinator.determinator import EncryptionDeterminator, EncrAnalyzeResult
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode
from src.main.app.file_service.file_reader import FileReader
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.words_service.word_loader import SimpleWordLoader


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
    determinator = EncryptionDeterminator(
        WordDictService(SimpleWordLoader('../../words_service/words_by_len.bin')),
        OperatingMode.OPTIMAL,
    )
    text = FileReader.read_file(f'../../../source/FOR_TEST_X/x.txt')
    # text = input().encode()

    result: EncrAnalyzeResult = determinator.determinate(text)

    print(f'\n1. Вырезано {result.cut_out_in_percent}%')
    print(f'2. HEX: {result.hex_verdict}')
    print(f'3. Etr: {result.entr_verdict}\n   {result.entropy_in_percent}% | {result.entropy_above_border_in_percent}%')


if __name__ == '__main__':
    main()
