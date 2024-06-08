import time
from os import listdir
from os.path import isfile, join

from src.main.app.model.extractors.token_extractor import TokenExtractor
from src.main.app.model.extractors.word_extractor import WordExtractor
from src.main.app.model.file_service.file_reader import FileReader
from src.main.app.model.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric, CalculatorLevenshteinMetric
from src.main.app.model.obfuscation.name_processor import NameProcessor
from src.main.app.model.obfuscation.obfuscation_determinator import ObfuscationDeterminator, ObfuscationResult
from src.main.app.model.obfuscation.searchers.searchers import VariableSearcher, FunctionSearcher, ClassSearcher
from src.main.app.model.settings.settings import Settings
from src.main.app.model.words_service.word_dict_service import WordDictService
from src.main.app.model.words_service.word_loader import SimpleWordLoader

SETTINGS_RAW = {
    "obfuscation": {
        "obfuscation_determinator": {
            "obf_text_border": 0.45,
            "obf_name_border": 0.50,
            "max_non_obf_count_digits": 4
        },
        "searcher_by_levenshtein_metric": {
            "mult_for_max_lev_distance": 0.38
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


def make_name_processor():
    tn_ext = TokenExtractor()
    var_searcher = VariableSearcher(tn_ext)
    func_searcher = FunctionSearcher(tn_ext)
    class_searcher = ClassSearcher(tn_ext)
    return NameProcessor([var_searcher, func_searcher, class_searcher], WordExtractor())


def make_searcher_by_levenshtein_metric(settings: Settings, word_dict_service):
    return SearcherByLevenshteinMetric(
        word_dict_service,
        CalculatorLevenshteinMetric(settings.analyzer_settings.calc_levenshtein_metric_settings),
        settings.analyzer_settings.searcher_levenshtein_metric_settings
    )


def main():
    settings = Settings(SETTINGS_RAW)
    word_dict_service = WordDictService(SimpleWordLoader(settings.analyzer_settings.word_loader_settings))
    determinator = ObfuscationDeterminator(
        name_processor=make_name_processor(),
        searcher_by_levenshtein_metric=make_searcher_by_levenshtein_metric(settings, word_dict_service),
        settings=settings.analyzer_settings.obf_determinator_settings
    )

    obf_files, no_obf_files = get_files_for_stat()
    total_count = len(obf_files) + len(no_obf_files)
    file_stat = open('../../../../source/obf_stat.txt', 'w')

    start = time.time()
    fp, tn, cur_count = process_files(total_count, 0, determinator, no_obf_files, file_stat)
    tp, fn, _ = process_files(total_count, cur_count, determinator, obf_files, file_stat)
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


def process_files(total_count, cur_count, determinator: ObfuscationDeterminator, filenames, file_stat):
    positive = negative = 0
    write_terminator_line(file_stat)
    for filename in filenames:
        result = determinator.determinate(FileReader.read_file(filename))
        write_result(result, file_stat, filename)
        if result.is_obf:
            positive += 1
        else:
            negative += 1
        cur_count += 1
        print(f'\r{round(100 * cur_count / total_count)}% : {filename}', end='')
    return positive, negative, cur_count


def get_files_for_stat():
    path_to_obf = [
        '../../../../source/obf/js',
        '../../../../source/obf/php',
        '../../../../source/obf/python',
    ]
    path_to_non_obf = [
        '../../../../source/obf_non/js',
        '../../../../source/obf_non/php',
        '../../../../source/obf_non/python',
    ]
    obf_files = get_filenames_by_path(path_to_obf)
    no_obf_files = get_filenames_by_path(path_to_non_obf)
    return obf_files, no_obf_files


def get_filenames_by_path(paths):
    filenames = list()
    for path in paths:
        filenames.extend(filter(isfile, (map(lambda f: join(path, f), listdir(path)))))
    return filenames


def write_terminator_line(file):
    file.write_results(f'{"=" * 52}\n{"=" * 52}\n\t\t\t\t\tНОВЫЙ РАЗДЕЛ\n{"=" * 52}\n{"=" * 52}\n\n')


def write_metrics(f_score, file_stat, fn, fp, precision, recall, tn, tp):
    file_stat.write_results(f'Вер. срабатывание: {tp} (TP)\n')
    file_stat.write_results(f'Лож. срабатывание: {fp} (FP)\n')
    file_stat.write_results(f'Вер. пропуск:      {tn} (TN)\n')
    file_stat.write_results(f'Лож. пропуск:      {fn} (FN))\n')
    file_stat.write_results(f'Точность = {round(100 * precision)}%\n')
    file_stat.write_results(f'Полнота = {round(100 * recall)}%\n')
    file_stat.write_results(f'F-score = {round(100 * f_score)}%\n')


def calc_metrics(fn, fp, tp):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * recall * precision / (recall + precision)
    return precision, recall, f_score


def write_result(result: ObfuscationResult, file_stat, filename):
    file_stat.write_results(f'ИМЯ: {filename}\n')
    file_stat.write_results(f'>{result.to_str()}\n')
    file_stat.write_results('\n' + '-' * 20 + '\n\n')


if __name__ == '__main__':
    main()
