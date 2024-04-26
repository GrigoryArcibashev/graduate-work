import time
from os import listdir
from os.path import isfile, join

from src.main.app.encryption.encryption_determinator.determinator import EncryptionDeterminator, EncrAnalyzeResult
from src.main.app.encryption.encryption_determinator.enums import OperatingMode
from src.main.app.file_reader import read_file
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.words_service.word_loader import SimpleWordLoader


def make_entropy_for_encr():
    word_dict_service = WordDictService(SimpleWordLoader('../words_service/words_by_len.bin'))
    # determinator = EncryptionDeterminator(
    #     OperatingMode.LOWER_STRICT,
    #     word_dict_service
    # )
    encr_files, no_encr_files = get_files_for_stat()
    total_count = len(encr_files) + len(no_encr_files)
    file_stat = open('../../source/encr_stat.txt', 'w')

    ###########
    best_f_score = 0
    best_recall = 0
    best_window_encryption_border = None
    best_unconditional_lower_bound_of_entropy = None
    best_conditional_lower_bound_of_entropy = None
    best_percent_of_entropy_vals_for_window = None

    webs = range(57, 62)
    ulboes = range(59, 65)
    clboes = range(54, 60)
    poevfws = range(40, 73, 3)

    TOTAL = len(webs) * len(ulboes) * len(clboes) * len(poevfws)
    CURENT = 0
    print(f'\r{round(100 * CURENT / TOTAL)}% ({CURENT}/{TOTAL})', end='')

    start = time.time()
    for web in webs:
        for ulboe in ulboes:
            for clboe in clboes:
                for poevfw in poevfws:
                    determinator = EncryptionDeterminator(
                        OperatingMode.LOWER_STRICT,
                        word_dict_service,
                        web, ulboe, clboe, poevfw
                    )

                    fp, tn, cur_count = process_files(total_count, 0, determinator, no_encr_files, file_stat)
                    tp, fn, _ = process_files(total_count, cur_count, determinator, encr_files, file_stat)
                    precision, recall, f_score = calc_metrics(fn, fp, tp)

                    ########################################################
                    if recall < best_recall:
                        continue
                    best_recall = recall
                    if f_score > best_f_score:
                        best_f_score = f_score
                    best_window_encryption_border = web
                    best_unconditional_lower_bound_of_entropy = ulboe
                    best_conditional_lower_bound_of_entropy = clboe
                    best_percent_of_entropy_vals_for_window = poevfw

                    CURENT += 1
                    print(f'\r{round(100 * CURENT / TOTAL)}% ({CURENT}/{TOTAL})', end='')
                    ########################################################

                    # write_metrics(f_score, file_stat, fn, fp, precision, recall, tn, tp)
    end = time.time()
    print(f'\nbest_recall = {round(100 * best_recall, 2)}%')
    print(f'best_f_score = {round(100 * best_f_score, 2)}%')
    print(f'best_window_encryption_border = {best_window_encryption_border}')
    print(f'best_unconditional_lower_bound_of_entropy = {best_unconditional_lower_bound_of_entropy}')
    print(f'best_conditional_lower_bound_of_entropy = {best_conditional_lower_bound_of_entropy}')
    print(f'best_percent_of_entropy_vals_for_window = {best_percent_of_entropy_vals_for_window}')
    ###########
    file_stat.close()

    # print(f'\nВер. срабатывание: {tp} (TP)')
    # print(f'Лож. срабатывание: {fp} (FP)')
    # print(f'Вер. пропуск:      {tn} (TN)')
    # print(f'Лож. пропуск:      {fn} (FN)')
    # print(f'Точность = {round(100 * precision, 2)}%')
    # print(f'Полнота =  {round(100 * recall, 2)}%')
    # print(f'F-score =  {round(100 * f_score, 2)}%')
    #
    print(f'\n{total_count} файлов - {round(end - start, 2)} сек.')


def process_files(total_count, cur_count, determinator, filenames, file_stat):
    positive = negative = 0
    # write_terminator_line(file_stat)
    for filename in filenames:
        result: EncrAnalyzeResult = determinator.determinate(read_file(filename))
        # write_result(result, file_stat, filename)
        if result.entr_verdict.is_encr or result.hex_verdict.is_encr:
            positive += 1
        else:
            negative += 1
        cur_count += 1
        # print(f'\r{round(100 * cur_count / total_count)}% : {filename}', end='')
    return positive, negative, cur_count


def get_files_for_stat():
    path_to_encr = [
        '../../source/encr/base32',
        '../../source/encr/base64',
        '../../source/encr/base85',
        '../../source/encr/base122',
        # '../../source/encr/rot13',
        # '../../source/encr/hex',
        '../../source/encr/AES',
        '../../source/encr/DES_triple',
    ]
    path_to_non_encr = [
        '../../source/encr_non/php',
        '../../source/encr_non/js',
        '../../source/encr_non/python',
        '../../source/encr_non/ruby',
        '../../source/encr_non/sharp',
        '../../source/encr_non/bash',
        '../../source/encr_non/html',
        '../../source/encr_non/css',
        '../../source/encr_non/xml',
        '../../source/encr_non/sql',
        '../../source/encr_non/other/arch',
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


def write_result(result: EncrAnalyzeResult, file_stat, filename):
    file_stat.write(f'ИМЯ: {filename}\n')
    file_stat.write(f'\tЭнтропия {result.entropy}% | {result.entropy_above_border}%\n')
    file_stat.write(f'\tВырезано {result.cut_out_in_percent}%\n')
    file_stat.write(f'{">ЕСТЬ ШИФР" if result.entr_verdict.is_encr or result.hex_verdict.is_encr else ">НЕТ ШИФРА"}\n')
    if result.entr_verdict.is_encr:
        file_stat.write(f'\t-Энтропия ({result.entr_verdict.to_str()})\n')
    if result.hex_verdict.is_encr:
        file_stat.write(f'\tHEX ({result.hex_verdict.to_str()})\n')
    file_stat.write('\n' + '-' * 20 + '\n\n')


if __name__ == '__main__':
    make_entropy_for_encr()
