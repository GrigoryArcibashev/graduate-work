import time
from os import listdir
from os.path import isfile, join

from src.main.app.model.encryption.encryption_determinator.determinator import EncryptionDeterminator, EncrAnalyzeResult
from src.main.app.model.file_service.file_reader import FileReader
from src.main.app.model.settings.settings import Settings
from src.main.app.model.words_service.word_dict_service import WordDictService
from src.main.app.model.words_service.word_loader import SimpleWordLoader

SETTINGS_RAW = {
    "hash": {
        "alg": "sha256",
        "algs": {
            "sha256": "sha256",
            "md5": "md5"
        }
    },
    "encryption": {
        "encryption_determinators": {
            "entropy": {
                "mode": "opt",
                "window_encryption_border": 60,
                "unconditional_lower_bound_of_entropy": 70,
                "conditional_lower_bound_of_entropy": 59,
                "percent_of_entropy_vals_for_window": 5,
                "upper_bound_of_entropy_optimal": 95,
                "upper_bound_of_entropy_strict": "+inf"
            },
            "hex": {
                "mode": "opt",
                "min_count_optimal": 3,
                "min_count_strict": 10
            },
            "modes": {
                "opt": "optimal",
                "str": "strict"
            }
        },
        "encryption_filter": {
            "encryption_boundary": 0.5,
            "save_del_size": 0.5
        },
        "entropy_analyzer": {
            "min_window_size": 100,
            "min_hope": 1,
            "divider_for_window": 120,
            "divider_for_hop": 5
        }
    },
    "obfuscation": {
        "obfuscation_determinator": {
            "obf_text_border": 0.4,
            "obf_name_border": 0.4,
            "max_non_obf_count_digits": 4
        },
        "searcher_by_levenshtein_metric": {
            "mult_for_max_lev_distance": 0.35
        },
        "calculator_levenshtein_metric": {
            "insert_cost": 1,
            "delete_cost": 1,
            "replace_cost": 1
        }
    },
    "word_loader": {
        "path_to_word_dict": "../../words_service/words_by_len.bin"
    }
}


def make_entropy_for_encr():
    settings = Settings(SETTINGS_RAW)
    word_dict_service = WordDictService(SimpleWordLoader(settings.analyzer_settings.word_loader_settings))
    determinator = EncryptionDeterminator(
        word_dict_service,
        settings.analyzer_settings.encr_determinator_entropy_settings,
        settings.analyzer_settings.encr_determinator_hex_settings,
        settings.analyzer_settings.entropy_analyzer_settings,
        settings.analyzer_settings.encr_filter_settings
    )
    encr_files, no_encr_files = get_files_for_stat()
    total_count = len(encr_files) + len(no_encr_files)
    file_stat = open('../../../../source/encr_stat.txt', 'w')

    start = time.time()
    fp, tn, cur_count = process_files(total_count, 0, determinator, no_encr_files, file_stat)
    tp, fn, _ = process_files(total_count, cur_count, determinator, encr_files, file_stat)
    precision, recall, f_score = calc_metrics(fn, fp, tp)
    end = time.time()

    write_metrics(f_score, file_stat, fn, fp, precision, recall, tn, tp)
    file_stat.close()

    print(f'\nВер. срабатывание: {tp} (TP)')
    print(f'Лож. срабатывание: {fp} (FP)')
    print(f'Вер. пропуск:      {tn} (TN)')
    print(f'Лож. пропуск:      {fn} (FN)')
    print(f'Точность = {round(100 * precision, 2)}%')
    print(f'Полнота =  {round(100 * recall, 2)}%')
    print(f'F-score =  {round(100 * f_score, 2)}%')
    print(f'\n{total_count} файлов - {round(end - start, 2)} сек.')


def process_files(total_count, cur_count, determinator, filenames, file_stat):
    positive = negative = 0
    write_terminator_line(file_stat)
    for filename in filenames:
        result: EncrAnalyzeResult = determinator.determinate(FileReader.read_file(filename))
        write_result(result, file_stat, filename)
        if result.entr_verdict.is_encr or result.hex_verdict.is_encr:
            positive += 1
        else:
            negative += 1
        cur_count += 1
        print(f'\r{round(100 * cur_count / total_count)}% : {filename}', end='')
    return positive, negative, cur_count


def get_files_for_stat():
    path_to_encr = [
        '../../../../source/encr/base32',
        '../../../../source/encr/base64',
        '../../../../source/encr/base85',
        '../../../../source/encr/base122',
        '../../../../source/encr/rot13',
        '../../../../source/encr/hex',
        '../../../../source/encr/AES',
        '../../../../source/encr/DES_triple',
    ]
    path_to_non_encr = [
        '../../../../source/encr_non/php',
        '../../../../source/encr_non/js',
        '../../../../source/encr_non/python',
        '../../../../source/encr_non/ruby',
        '../../../../source/encr_non/sharp',
        '../../../../source/encr_non/bash',
        '../../../../source/encr_non/html',
        '../../../../source/encr_non/css',
        '../../../../source/encr_non/xml',
        '../../../../source/encr_non/sql',
        '../../../../source/encr_non/other/arch',
        '../../../../source/encr_non/other/img',
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
    file_stat.write(f'\tЭнтропия {result.entropy_in_percent}% | {result.entropy_above_border_in_percent}%\n')
    file_stat.write(f'\tВырезано {result.cut_out_in_percent}%\n')
    file_stat.write(f'{">ЕСТЬ ШИФР" if result.entr_verdict.is_encr or result.hex_verdict.is_encr else ">НЕТ ШИФРА"}\n')
    if result.entr_verdict.is_encr:
        file_stat.write(f'\t-Энтропия ({result.entr_verdict.to_str()})\n')
    if result.hex_verdict.is_encr:
        file_stat.write(f'\t-HEX ({result.hex_verdict.to_str()})\n')
    file_stat.write('\n' + '-' * 20 + '\n\n')


if __name__ == '__main__':
    make_entropy_for_encr()
