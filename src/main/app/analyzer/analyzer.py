import time
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from os.path import isfile, join

from src.main.app.encryption.encryption_determinator.determinator import EncryptionDeterminator, EncrAnalyzeResult
from src.main.app.encryption.encryption_determinator.enums import OperatingMode
from src.main.app.extractors.token_extractor import TokenExtractor
from src.main.app.extractors.word_extractor import WordExtractor
from src.main.app.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.obfuscation.name_processor import NameProcessor
from src.main.app.obfuscation.obfuscation_determinator import ObfuscationDeterminator
from src.main.app.obfuscation.searchers.searchers import VariableSearcher, FunctionSearcher, ClassSearcher
from src.main.app.suspicious.searcher import SuspySearcher
from src.main.app.suspicious.suspicious_code import SuspiciousCode
from src.main.app.util.file_reader import read_file
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.words_service.word_loader import SimpleWordLoader


class AnalysisResult:
    def __init__(self, encr_res: EncrAnalyzeResult, obf_res: bool, suspy_res: list[SuspiciousCode]):
        self._encr_res = encr_res
        self._obf_res = obf_res
        self._suspy_res = suspy_res

    @property
    def encr_res(self) -> EncrAnalyzeResult:
        return self._encr_res

    @property
    def obf_res(self) -> bool:
        return self._obf_res

    @property
    def suspy_res(self) -> list[SuspiciousCode]:
        return self._suspy_res

    def to_str(self) -> str:
        return self._encr_res_to_str() + self._obf_res_to_str() + self._suspy_res_to_str()

    def _encr_res_to_str(self) -> str:
        result = ['\nПОИСК ШИФРА', ]
        if self.encr_res.entr_verdict.is_encr or self.encr_res.hex_verdict.is_encr:
            result.append(f'\tЕСТЬ ШИФР')
        else:
            result.append('\tНЕТ ШИФРА')
        if self.encr_res.entr_verdict.is_encr:
            result.append(f'\t  +Энтропия ({self.encr_res.entr_verdict.to_str()})')
            result.append(f'\t\t(энт. {self.encr_res.entropy}% | {self.encr_res.entropy_above_border}%)')
            result.append(f'\t\t(выр. {self.encr_res.cut_out_in_percent}%)')
        if self.encr_res.hex_verdict.is_encr:
            result.append(f'\t  +HEX ({self.encr_res.hex_verdict.to_str()})')
        return '\n'.join(result) + '\n'

    def _obf_res_to_str(self) -> str:
        result = ['\nПОИСК ОБФУСКАЦИИ', ]
        if self.obf_res:
            result.append(f'\tЕСТЬ ОБФ.')
        else:
            result.append('\tНЕТ ОБФ.')
        return '\n'.join(result) + '\n'

    def _suspy_res_to_str(self) -> str:
        result = ['\nПОИСК ПОДОЗРИТЕЛЬНЫХ КОМАНД', ]
        if not self.suspy_res:
            result.append('\tНЕ НАЙДЕНО')
        else:
            for suspy in self.suspy_res:
                result.append(f'\t{suspy}')
        return '\n'.join(result) + '\n'

    def __str__(self):
        return self.to_str()


class Analyzer:
    def __init__(
            self,
            path_to_dict: str,
            encr_mode: OperatingMode = OperatingMode.OPTIMAL
    ):
        word_dict_service = WordDictService(SimpleWordLoader(path_to_dict))
        self._encr_determinator = EncryptionDeterminator(word_dict_service, encr_mode)
        self._obf_determinator = ObfuscationDeterminator(
            name_processor=self._built_name_processor(),
            searcher_by_levenshtein_metric=SearcherByLevenshteinMetric(word_dict_service)
        )
        self._suspy_searcher = SuspySearcher()

    @staticmethod
    def _built_name_processor() -> NameProcessor:
        var_searcher = VariableSearcher(TokenExtractor())
        func_searcher = FunctionSearcher(TokenExtractor())
        class_searcher = ClassSearcher(TokenExtractor())
        name_processor = NameProcessor([var_searcher, func_searcher, class_searcher], WordExtractor())
        return name_processor

    def analyze(self, data: bytes) -> AnalysisResult:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_encr = executor.submit(self._encr_determinator.determinate, data)
            future_obf = executor.submit(self._obf_determinator.determinate, data)
            future_suspy = executor.submit(self._suspy_searcher.search, data)

            return AnalysisResult(future_encr.result(), future_obf.result(), future_suspy.result())


def get_filenames(paths):
    filenames = list()
    for path in paths:
        filenames.extend(filter(isfile, (map(lambda f: join(path, f), listdir(path)))))
    return filenames


def sec_to_str_min_and_sec(sec: float) -> str:
    if sec < 60:
        return f'{int(sec)} сек.'
    return f'{int(sec // 60)} мин. {int(sec % 60)} сек.'


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
    analyzer = Analyzer(path_to_dict='../words_service/words_by_len.bin')

    processed = 0
    total = len(filenames)
    expected_time = 1.07 * total
    start = time.time()
    print(
        f'\r{round(100 * processed / total)}% ({processed}/{total}), осталось < '
        + f'{sec_to_str_min_and_sec(expected_time - (time.time() - start))}',
        end=''
    )
    for filename in filenames:
        analyzer.analyze(read_file(filename))
        processed += 1
        print(
            f'\r{round(100 * processed / total)}% ({processed}/{total}), осталось < '
            + f'{sec_to_str_min_and_sec(expected_time - (time.time() - start))}',
            end=''
        )
    all_time = time.time() - start

    print(f'\nВРЕМЯ: {sec_to_str_min_and_sec(all_time)}')
    print(f'~{round(all_time / total, 2)} сек. на файл')


if __name__ == '__main__':
    main()
