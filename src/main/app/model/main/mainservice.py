from typing import Optional

from src.main.app.model.analyzer.analyzer import Analyzer
from src.main.app.model.db_service.converter import ConverterForDB
from src.main.app.model.db_service.result_of_file_analysis import ResultOfFileAnalysis, FileModStatus
from src.main.app.model.db_service.rw_service import DBService
from src.main.app.model.file_service.file_explorer import FileExplorer
from src.main.app.model.file_service.file_reader import FileReader
from src.main.app.model.hasher.hash_service import Hasher, HashResult
from src.main.app.model.settings.settings import Settings


class MainService:
    def __init__(self, settings: Settings, root_dir: str, path_to_db: str):
        self._root_dir = root_dir
        self._hasher = Hasher(settings.hasher_settings)
        self._analyzer = Analyzer(settings.analyzer_settings)
        self._db_service = DBService(path_to_db)

    @property
    def root_dir(self) -> str:
        return self._root_dir

    @root_dir.setter
    def root_dir(self, new_value: str) -> None:
        self._root_dir = new_value

    def get_results_from_db(self) -> list[ResultOfFileAnalysis]:
        return ConverterForDB.convert_from_db_models(self._db_service.read())

    def mark_files_as_trusted(
            self,
            results_of_file_analysis: list[ResultOfFileAnalysis],
            trusted_files: set[str]
    ) -> None:
        results_to_db: list[ResultOfFileAnalysis] = list()
        for result in results_of_file_analysis:
            if result.filename in trusted_files:
                status = FileModStatus.TRUSTED
            else:
                status = FileModStatus.MODIFIED if result.status == FileModStatus.MODIFIED else FileModStatus.UNTRUSTED
            new_result = ResultOfFileAnalysis(result.filename, result.an_result, result.hash, status)
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
            hash_fin = _hash
            status = FileModStatus.UNTRUSTED
            print(f'{filename} db_result is None')
        elif db_result.hash == _hash:
            # файл не изменился, сохраняем статус
            filename = filename
            an_result = db_result.an_result
            hash_fin = db_result.hash
            status = db_result.status
            print(f'{filename} db_result.hash == _hash')
        elif db_result.hash != _hash:
            # файл изменился, устанавливаем новый статус
            filename = filename
            an_result = self._analyzer.analyze(data)
            hash_fin = _hash
            status = FileModStatus.MODIFIED
            print(f'{filename} db_result.hash != _hash')
        else:
            print(f'{filename} {self.__class__}')
            raise Exception()
        return ResultOfFileAnalysis(
            filename=filename,
            an_result=an_result,
            _hash=hash_fin,
            status=status
        )

    @staticmethod
    def _make_dict_filename_to_result(results: list[ResultOfFileAnalysis]) -> dict[str, ResultOfFileAnalysis]:
        return {result.filename: result for result in results}


def main_app():
    settings = Settings(FileReader.read_json('../../../settings.json'))
    app = MainService(
        settings=settings,
        root_dir='../../../source/obf/',
        path_to_db='sqlite:///../../../database.db')
    app.run()
    print('=' * 70)
    results = app.get_results_from_db()
    app.mark_files_as_trusted(results, {res.filename for res in results})
    for res in app.get_results_from_db():
        print(f'{res.filename} - {res.status}')
        # print(res, end='\n\n')


if __name__ == '__main__':
    # main()
    main_app()
