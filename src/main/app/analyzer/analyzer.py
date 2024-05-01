from concurrent.futures import ThreadPoolExecutor

from src.main.app.analyzer.analysis_result import AnalysisResult
from src.main.app.encryption.encryption_determinator.determinator import EncryptionDeterminator
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode
from src.main.app.extractors.token_extractor import TokenExtractor
from src.main.app.extractors.word_extractor import WordExtractor
from src.main.app.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.obfuscation.name_processor import NameProcessor
from src.main.app.obfuscation.obfuscation_determinator import ObfuscationDeterminator
from src.main.app.obfuscation.searchers.searchers import VariableSearcher, FunctionSearcher, ClassSearcher
from src.main.app.suspicious.searcher import SuspySearcher
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.words_service.word_loader import SimpleWordLoader


class Analyzer:
    def __init__(
            self,
            path_to_dict: str,
            encr_entr_mode: OperatingMode,
            encr_hex_mode: OperatingMode,
    ):
        word_dict_service = WordDictService(SimpleWordLoader(path_to_dict))
        self._encr_determinator = EncryptionDeterminator(word_dict_service, encr_entr_mode, encr_hex_mode)
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
