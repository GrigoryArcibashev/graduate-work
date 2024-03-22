from src.main.app.encryption.encr_filter.encryption_filter import EncryptionFilter
from src.main.app.encryption.encr_filter.words.word_loader import SimpleWordLoader
from src.main.app.encryption.encr_filter.words.word_provider import WordProvider
from src.main.app.encryption.entropy.entropy import Entropy
from src.main.app.encryption.entropy.entropy_analyzer import EntropyAnalyzer
from src.main.app.file_reader import read_file


class EncryptionDeterminator:
    def __init__(self, entropy_analyzer):
        self._entropy_analyzer = entropy_analyzer
        self._window_encryption_border = 60

    def determinate(self, data):
        entropy = self._entropy_analyzer.analyze(data)
        entropies, window_size, hop = self._entropy_analyzer.window_analyze(data)
        count_above_border = len(list(filter(lambda entr: entr >= self._window_encryption_border, entropies)))
        entropy_above_border = round(100 * count_above_border / len(entropies))
        if entropy >= 70 or entropy >= 65 and entropy_above_border >= 55:
            return True, entropy, entropy_above_border
        return False, entropy, entropy_above_border


def make_stat():
    tp = tn = fp = fn = 0

    ed = EncryptionDeterminator(EntropyAnalyzer(Entropy()))
    ef = EncryptionFilter(WordProvider(SimpleWordLoader('encr_filter/words/words.txt')))
    prefixes = ['../../source/orig/', '../../source/encr/']
    postfix = '.txt'
    files = [str(i) for i in range(1, 21)]

    with open('../../source/encr_stat.txt', 'w') as file_stat:
        for prefix in prefixes:
            for filename in files:
                text = list(read_file(prefix + filename + postfix))
                filtered_text = ef.filter(text)
                is_encr, entropy, entropy_above_border = ed.determinate(filtered_text)
                if prefix == prefixes[0]:
                    # шифра быть не должно
                    if is_encr:
                        fp += 1
                    else:
                        tn += 1
                else:
                    # шифр должен быть
                    if is_encr:
                        tp += 1
                    else:
                        fn += 1

                file_stat.write(f'ИМЯ ФАЙЛА: {prefix + filename + postfix}\n')
                file_stat.write(f'\tЭнтропия = {entropy}%\n')
                file_stat.write(f'\tВыше черты = {entropy_above_border}%\n')
                file_stat.write(f'ИТОГ: {"YES" if is_encr else "NO"}\n\n')
            file_stat.write('-' * 20 + '\n\n')

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f_score = 2 * recall * precision / (recall + precision)

        file_stat.write(f'TP {tp}\nTN {tn}\nFP {fp}\nFN {fn}\n')
        file_stat.write(f'Точность = {round(100 * precision)}%\n')
        file_stat.write(f'Полнота = {round(100 * recall)}%\n')
        file_stat.write(f'F-score = {round(100 * f_score)}%\n')

        print(f'TP {tp}\nTN {tn}\nFP {fp}\nFN {fn}')
        print(f'Точность = {round(100 * precision)}%')
        print(f'Полнота = {round(100 * recall)}%')
        print(f'F-score = {round(100 * f_score)}%')


if __name__ == '__main__':
    make_stat()
