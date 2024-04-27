import time
from os import listdir
from os.path import isfile, join
from typing import Iterator

from src.main.app.analyzer.analysis_result import AnalysisResult
from src.main.app.analyzer.analyzer import Analyzer
from src.main.app.util.file_reader import read_file


def get_filenames(paths: list[str]) -> list[str]:
    filenames = list()
    for path in paths:
        filenames.extend(filter(isfile, (map(lambda f: join(path, f), listdir(path)))))
    return filenames


def sec_to_str_min_and_sec(sec: float) -> str:
    if sec < 60:
        return f'{int(sec)} сек.'
    return f'{int(sec // 60)} мин. {int(sec % 60)} сек.'


def print_time_results(all_time, total) -> None:
    print(f'\nВРЕМЯ: {sec_to_str_min_and_sec(all_time)}')
    print(f'~{round(all_time / total, 2)} сек. на файл')


def print_state(processed, total, start) -> None:
    if processed:
        velocity = (time.time() - start) / processed
        end = f', осталось ~ {sec_to_str_min_and_sec((total - processed) * velocity)}'
    else:
        end = ''
    print(f'\r{round(100 * processed / total)}% ({processed}/{total})', end=end)


def print_analyze_results(results: list[(str, AnalysisResult)], inp: bool = False) -> None:
    for filename, result in results:
        if not result.suspy_res:
            continue
        if inp:
            input('\n<<ДАЛЕЕ (Enter)>>')
        else:
            print('=' * 40)
        print(f'ИМЯ: {filename}')
        print(result)


def run_analyzer(filenames: list[str], path_to_dict: str) -> Iterator[AnalysisResult]:
    analyzer = Analyzer(path_to_dict=path_to_dict)
    for filename in filenames:
        yield analyzer.analyze(read_file(filename))


def main():
    paths = [
        '../../source/encr/base32',
        '../../source/encr/base64',
        '../../source/encr/base85',
        '../../source/encr/base122',
        '../../source/encr/rot13',
        '../../source/encr/hex',
        '../../source/encr/AES',
        '../../source/encr/DES_triple',
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
        '../../source/encr_non/other/img',
    ]
    filenames = get_filenames(paths)
    path_to_dict = '../words_service/words_by_len.bin'

    results = list()
    processed = 0
    total = len(filenames)
    start = time.time()
    print_state(processed, total, start)
    for result in run_analyzer(filenames, path_to_dict):
        results.append((filenames[processed], result))
        processed += 1
        print_state(processed, total, start)
    print_time_results(time.time() - start, total)
    print_analyze_results(results, inp=False)


if __name__ == '__main__':
    main()
