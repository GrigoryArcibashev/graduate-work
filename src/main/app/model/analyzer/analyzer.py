from concurrent.futures import ThreadPoolExecutor

from src.main.app.model.analyzer.analysis_result import AnalysisResult
from src.main.app.model.encryption.encryption_determinator.determinator import EncryptionDeterminator
from src.main.app.model.extractors.token_extractor import TokenExtractor
from src.main.app.model.extractors.word_extractor import WordExtractor
from src.main.app.model.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric, CalculatorLevenshteinMetric
from src.main.app.model.obfuscation.name_processor import NameProcessor
from src.main.app.model.obfuscation.obfuscation_determinator import ObfuscationDeterminator
from src.main.app.model.obfuscation.searchers.searchers import VariableSearcher, FunctionSearcher, ClassSearcher
from src.main.app.model.settings.analyzer_settings import AnalyzerSettings
from src.main.app.model.suspicious.searcher import SuspySearcher
from src.main.app.model.words_service.word_dict_service import WordDictService
from src.main.app.model.words_service.word_loader import SimpleWordLoader


class Analyzer:
    def __init__(self, settings: AnalyzerSettings):
        word_dict_service = WordDictService(SimpleWordLoader(settings.word_loader_settings))
        self._encr_determinator = EncryptionDeterminator(
            word_dict_service=word_dict_service,
            entropy_det_settings=settings.encr_determinator_entropy_settings,
            hex_det_settings=settings.encr_determinator_hex_settings,
            entropy_analyzer_settings=settings.entropy_analyzer_settings,
            encr_filter_settings=settings.encr_filter_settings
        )
        self._obf_determinator = ObfuscationDeterminator(
            name_processor=self._built_name_processor(),
            searcher_by_levenshtein_metric=SearcherByLevenshteinMetric(
                word_dict_service=word_dict_service,
                metric_calculator=CalculatorLevenshteinMetric(settings.calc_levenshtein_metric_settings),
                settings=settings.searcher_levenshtein_metric_settings
            ),
            settings=settings.obf_determinator_settings
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
