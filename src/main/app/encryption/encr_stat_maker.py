from os import listdir
from os.path import isfile, join
from src.main.app.encryption.encryption_filter import EncryptionFilter
from src.main.app.words_service.word_loader import SimpleWordLoader
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.encryption.encryption_determinator import EncryptionDeterminatorByEntropy, EncryptionDeterminatorByHEX
from src.main.app.encryption.entropy.entropy import Entropy
from src.main.app.encryption.entropy.entropy_analyzer import EntropyAnalyzer
from src.main.app.file_reader import read_file


def make_entropy_for_encr():
    tp = tn = fp = fn = 0

    ed_entropy = EncryptionDeterminatorByEntropy(EntropyAnalyzer(Entropy()))
    ed_hex = EncryptionDeterminatorByHEX()
    ef = EncryptionFilter(WordDictService(SimpleWordLoader('../words_service/words_by_len.bin')))

    encr_files, no_encr_files = get_files_for_stat()
    total_count = len(encr_files) + len(no_encr_files)
    cur_count = 0

    file_stat = open('../../source/encr_stat.txt', 'w')
    write_terminator_line(file_stat)
    for filename in no_encr_files:
        cut_out, entropy, entropy_above_border, is_encr, is_hex_encr = determinate(ed_entropy, ed_hex, ef, filename)
        write_result(cut_out, entropy, entropy_above_border, file_stat, filename, is_encr, is_hex_encr)
        if is_encr or is_hex_encr:
            fp += 1
        else:
            tn += 1
        cur_count += 1
        print(f'\r{round(100 * cur_count / total_count)}% : {filename}', end='')
    write_terminator_line(file_stat)
    for filename in encr_files:
        cut_out, entropy, entropy_above_border, is_encr, is_hex_encr = determinate(ed_entropy, ed_hex, ef, filename)
        write_result(cut_out, entropy, entropy_above_border, file_stat, filename, is_encr, is_hex_encr)
        if is_encr or is_hex_encr:
            tp += 1
        else:
            fn += 1
        cur_count += 1
        print(f'\r{round(100 * cur_count / total_count)}% : {filename}', end='')
    print()

    precision, recall, f_score = calc_metrics(fn, fp, tp)
    write_metrics(f_score, file_stat, fn, fp, precision, recall, tn, tp)
    file_stat.close()

    print(f'Вер. срабатывание: {tp} (TP)')
    print(f'Лож. срабатывание: {fp} (FP)')
    print(f'Вер. пропуск:      {tn} (TN)')
    print(f'Лож. пропуск:      {fn} (FN)')
    print(f'Точность = {round(100 * precision, 2)}%')
    print(f'Полнота =  {round(100 * recall, 2)}%')
    print(f'F-score =  {round(100 * f_score, 2)}%')


def get_files_for_stat():
    path_to_encr = ['../../source/encr/']
    path_to_non_encr = [
        '../../source/encr_non/php',
        '../../source/encr_non/js',
        '../../source/encr_non/py',
        '../../source/encr_non/ruby',
        '../../source/encr_non/sharp',
        '../../source/encr_non/bash',
        '../../source/encr_non/html',
        '../../source/encr_non/css',
        '../../source/encr_non/xml',
        '../../source/encr_non/sql',
        # '../../source/encr_non/other/arch',
        # '../../source/encr_non/other/img',
    ]
    encr_files = get_filenames_by_path(path_to_encr)
    no_encr_files = get_filenames_by_path(path_to_non_encr)
    return encr_files, no_encr_files


def get_filenames_by_path(paths):
    filenames = list()
    for path in paths:
        filenames.extend(filter(isfile, (map(lambda f: join(path, f), listdir(path)))))
    return filenames


def write_terminator_line(file):
    file.write(f'{"=" * 52}\n{"=" * 52}\n\t\t\t\t\tНОВЫЙ РАЗДЕЛ\n{"=" * 52}\n{"=" * 52}\n\n')


def write_metrics(f_score, file_stat, fn, fp, precision, recall, tn, tp):
    file_stat.write(f'Вер. срабатывание: {tp} (TP)\n')
    file_stat.write(f'Лож. срабатывание: {fp} (FP)\n')
    file_stat.write(f'Вер. пропуск:      {tn} (TN)\n')
    file_stat.write(f'Лож. пропуск:      {fn} (FN))\n')
    file_stat.write(f'Точность = {round(100 * precision)}%\n')
    file_stat.write(f'Полнота = {round(100 * recall)}%\n')
    file_stat.write(f'F-score = {round(100 * f_score)}%\n')


def calc_metrics(fn, fp, tp):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * recall * precision / (recall + precision)
    return precision, recall, f_score


def determinate(ed_en, ed_hex, ef, filename):
    text = read_file(filename)
    is_hex_encr = ed_hex.determinate(text)
    bytes_text = list(text)
    len_before = len(bytes_text)
    filtered_text = ef.filter(bytes_text)
    cut_out = round(100 - len(filtered_text) / (max(1.0, len_before / 100)), 2)
    is_encr, entropy, entropy_above_border = ed_en.determinate(filtered_text)
    return cut_out, entropy, entropy_above_border, is_encr, is_hex_encr


def write_result(cut_out, entropy, entropy_above_border, file_stat, filename, is_encr, is_hex_encr):
    file_stat.write(f'ИМЯ: {filename}\n')
    file_stat.write(f'\tЭнтропия {entropy}% | {entropy_above_border}%\n')
    file_stat.write(f'\tВырезано {cut_out}%\n')
    file_stat.write(f'{">ЕСТЬ ШИФР" if is_encr or is_hex_encr else ">НЕТ ШИФРА"}\n')
    if is_encr:
        file_stat.write(f'\t-Энтропия\n')
    if is_hex_encr:
        file_stat.write(f'\tHEX\n')
    file_stat.write('\n' + '-' * 20 + '\n\n')


if __name__ == '__main__':
    make_entropy_for_encr()
