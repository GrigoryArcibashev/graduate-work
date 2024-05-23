import time
from os import listdir
from os.path import isfile, join

from src.main.app.analyzer.analysis_result import AnalysisResult
from src.main.app.analyzer.analyzer import Analyzer
from src.main.app.db_service.read_upd_service import DBService
from src.main.app.hasher.hash_service import Hasher
from src.main.app.settings.settings import Settings
from src.main.app.file_service.file_reader import FileReader


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
    print(f'~{round(all_time / max(1, total), 2)} сек. на файл')


def print_state(processed, total, start, filename=None) -> None:
    if processed:
        velocity = (time.time() - start) / processed
        end = f', осталось ~ {sec_to_str_min_and_sec((total - processed) * velocity)}'
        end += f' ({filename})' if filename else f''
    else:
        end = ''
    print(f'\r{round(100 * processed / max(1, total))}% ({processed}/{total})', end=end)


def print_analyze_results(results: list[(str, AnalysisResult)], inp: bool = False) -> None:
    for filename, result in results:
        # if not result.obf_res.is_obf:
        #     continue
        if inp:
            input('\n<<ДАЛЕЕ (Enter)>>')
        else:
            print('=' * 40)
        print(f'ИМЯ: {filename}')
        print(result)


def run(filenames: list[str], analyzer: Analyzer) -> list[AnalysisResult]:
    for filename in filenames:
        yield analyzer.analyze(FileReader.read_file(filename))


def main():
    paths = [
        # '../../source/FOR_TEST_X',

        '../../source/obf/js',
        '../../source/obf/php',
        '../../source/obf/sharp',
        '../../source/obf/python',
        #
        '../../source/obf_non/js',
        '../../source/obf_non/php',
        '../../source/obf_non/sharp',
        '../../source/obf_non/python',
        #
        '../../source/encr/base32',
        '../../source/encr/base64',
        '../../source/encr/base85',
        '../../source/encr/base122',
        '../../source/encr/rot13',
        '../../source/encr/hex',
        '../../source/encr/AES',
        '../../source/encr/DES_triple',
        #
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
    analyzer = Analyzer(Settings(FileReader.read_json('../../settings.json')).analyzer_settings)

    results = list()
    processed = 0
    total = len(filenames)
    start = time.time()
    print_state(processed, total, start, filenames[processed])
    for result in run(filenames, analyzer):
        results.append((filenames[processed], result))
        processed += 1
        print_state(processed, total, start, filename=filenames[processed] if processed < total else None)
    print_time_results(time.time() - start, total)
    print_analyze_results(results, inp=False)


class App:
    def __init__(self, settings: Settings, root_dir: str, path_to_db: str):
        self._root_dir = root_dir
        self._path_to_db = path_to_db
        self._hasher = Hasher(settings.hasher_settings)
        self._analyzer = Analyzer(settings.analyzer_settings)
        self._db_service = DBService(path_to_db)

    def run(self):
        # прочитать данные из БД (ЕСЛИ ЕСТЬ)
        # проанализировать файлы
        # сравнить результаты анализа
        # обновить БД
        pass

    def get_results_from_db(self):
        # прочитать данные из БД (ЕСЛИ ЕСТЬ)
        # вернуть результат
        pass


if __name__ == '__main__':
    main()