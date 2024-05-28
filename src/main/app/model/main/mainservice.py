import time
from os import listdir
from os.path import isfile, join
from typing import Optional

from src.main.app.model.analyzer.analysis_result import AnalysisResult
from src.main.app.model.analyzer.analyzer import Analyzer
from src.main.app.model.db_service.converter import ConverterForDB, ResultOfFileAnalysis
from src.main.app.model.db_service.rw_service import DBService
from src.main.app.model.file_service.file_explorer import FileExplorer
from src.main.app.model.file_service.file_reader import FileReader
from src.main.app.model.hasher.hash_service import Hasher, HashResult
from src.main.app.model.settings.settings import Settings


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
        '../../source/FOR_TEST_X',
        #
        # '../../source/obf/js',
        # '../../source/obf/php',
        # '../../source/obf/sharp',
        # '../../source/obf/python',

        # '../../source/obf_non/js',
        # '../../source/obf_non/php',
        # '../../source/obf_non/sharp',
        # '../../source/obf_non/python',

        # '../../source/encr/base32',
        # '../../source/encr/base64',
        # '../../source/encr/base85',
        # '../../source/encr/base122',
        # '../../source/encr/rot13',
        # '../../source/encr/hex',
        # '../../source/encr/AES',
        # '../../source/encr/DES_triple',

        # '../../source/encr_non/php',
        # '../../source/encr_non/js',
        # '../../source/encr_non/python',
        # '../../source/encr_non/ruby',
        # '../../source/encr_non/sharp',
        # '../../source/encr_non/bash',
        # '../../source/encr_non/html',
        # '../../source/encr_non/css',
        # '../../source/encr_non/xml',
        # '../../source/encr_non/sql',
        # '../../source/encr_non/other/arch',
        # '../../source/encr_non/other/img',
    ]
    filenames = get_filenames(paths)
    settings = Settings(FileReader.read_json('../../settings.json'))
    analyzer = Analyzer(settings.analyzer_settings)

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


class MainService:
    def __init__(self, settings: Settings, root_dir: str, path_to_db: str):
        self._root_dir = root_dir
        self._hasher = Hasher(settings.hasher_settings)
        self._analyzer = Analyzer(settings.analyzer_settings)
        self._db_service = DBService(path_to_db)

    def get_results_from_db(self) -> list[ResultOfFileAnalysis]:
        return ConverterForDB.convert_from_db_models(self._db_service.read())

    def mark_files_as_trusted(
            self,
            results_of_file_analysis: list[ResultOfFileAnalysis],
            trusted_files: set[str]
    ) -> None:
        results_to_db: list[ResultOfFileAnalysis] = list()
        for result in results_of_file_analysis:
            if result.filename not in trusted_files:
                results_to_db.append(result)
                continue
            new_result = ResultOfFileAnalysis(
                filename=result.filename,
                an_result=result.an_result,
                old_hash=result.old_hash if result.new_hash is None else result.new_hash,
                new_hash=None
            )
            results_to_db.append(new_result)
        self._db_service.write(ConverterForDB.convert_to_db_models(results_to_db))

    def run(self) -> None:
        results_from_db = self._make_dict_filename_to_result(self.get_results_from_db())
        results_to_db: list[ResultOfFileAnalysis] = list()
        for filename in FileExplorer.get_all_filenames(self._root_dir, recursive=True):
            data = FileReader.read_file(filename)
            _hash: HashResult = self._hasher.calc_hash(data)
            db_result = results_from_db.get(filename)
            results_to_db.append(self._make_new_result_for_db(filename, _hash, data, db_result))
        self._db_service.write(ConverterForDB.convert_to_db_models(results_to_db))

    def _make_new_result_for_db(
            self,
            filename: str,
            _hash: HashResult,
            data: bytes,
            db_result: Optional[ResultOfFileAnalysis]
    ) -> ResultOfFileAnalysis:
        if db_result is None:
            # файл новый, его в БД не было
            filename = filename
            an_result = self._analyzer.analyze(data)
            old_hash = None
            new_hash = _hash
            print(f'{filename} db_result is None')
        elif db_result.old_hash == _hash:
            # файл не изменился, он всё еще доверенный
            filename = filename
            an_result = db_result.an_result if db_result.new_hash is None else self._analyzer.analyze(data)
            old_hash = db_result.old_hash
            new_hash = None
            print(f'{filename} db_result.old_hash == _hash | {db_result.new_hash is None} = db_result.new_hash is None')
        elif db_result.new_hash == _hash:
            # файл не изменился с последнего запуска, НО он НЕ доверенный
            filename = filename
            an_result = db_result.an_result
            old_hash = db_result.old_hash
            new_hash = db_result.new_hash
            print(f'{filename} db_result.new_hash == _hash')
        elif db_result.new_hash != _hash:
            # файл изменился, он НЕ доверенный
            filename = filename
            an_result = self._analyzer.analyze(data)
            old_hash = db_result.old_hash
            new_hash = _hash
            print(f'{filename} db_result.new_hash != _hash')
        else:
            print(f'{filename} {self.__class__}')
            raise Exception()
        return ResultOfFileAnalysis(
            filename=filename,
            an_result=an_result,
            old_hash=old_hash,
            new_hash=new_hash
        )

    @staticmethod
    def _make_dict_filename_to_result(results: list[ResultOfFileAnalysis]) -> dict[str, ResultOfFileAnalysis]:
        return {result.filename: result for result in results}


def main_app():
    settings = Settings(FileReader.read_json('../../../settings.json'))
    app = MainService(
        settings=settings,
        root_dir='../../../source/FOR_TEST_X',
        path_to_db='sqlite:///../../../database.db')
    app.run()
    # print('=' * 70)
    # results = app.get_results_from_db()
    # app.mark_files_as_trusted(results, {res.filename for res in results})
    # for res in app.get_results_from_db():
    #     print(res, end='\n\n')


if __name__ == '__main__':
    # main()
    main_app()
