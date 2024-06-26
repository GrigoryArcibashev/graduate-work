from src.main.app.model.settings.calculator_levenshtein_metric_settings import CalculatorLevenshteinMetricSettings
from src.main.app.model.settings.encr_entropy_settings import EncrDetEntropySettings
from src.main.app.model.settings.encr_filter_settings import EncrFilterSettings
from src.main.app.model.settings.encr_hex_settings import EncrDetHEXSettings
from src.main.app.model.settings.entropy_analyzer_settings import EntropyAnalyzerSettings
from src.main.app.model.settings.obfuscation_determinator_settings import ObfuscationDetSettings
from src.main.app.model.settings.searcher_levenshtein_metric_settings import SearcherLevenshteinMetricSettings
from src.main.app.model.settings.word_loader_settings import WordLoaderSettings


class AnalyzerSettings:
    def __init__(self, raw_settings: dict):
        self._raw_settings = raw_settings

    @property
    def encr_determinator_entropy_settings(self) -> EncrDetEntropySettings:
        return EncrDetEntropySettings(
            self._raw_settings['encryption']['encryption_determinators']['entropy'],
            self._raw_settings['encryption']['encryption_determinators']['modes']
        )

    @property
    def encr_determinator_hex_settings(self) -> EncrDetHEXSettings:
        return EncrDetHEXSettings(
            self._raw_settings['encryption']['encryption_determinators']['hex'],
            self._raw_settings['encryption']['encryption_determinators']['modes']
        )

    @property
    def encr_filter_settings(self) -> EncrFilterSettings:
        return EncrFilterSettings(self._raw_settings['encryption']['encryption_filter'])

    @property
    def entropy_analyzer_settings(self) -> EntropyAnalyzerSettings:
        return EntropyAnalyzerSettings(self._raw_settings['encryption']['entropy_analyzer'])

    @property
    def obf_determinator_settings(self) -> ObfuscationDetSettings:
        return ObfuscationDetSettings(self._raw_settings['obfuscation']['obfuscation_determinator'])

    @property
    def calc_levenshtein_metric_settings(self) -> CalculatorLevenshteinMetricSettings:
        return CalculatorLevenshteinMetricSettings(
            self._raw_settings['obfuscation']['calculator_levenshtein_metric'])

    @property
    def searcher_levenshtein_metric_settings(self) -> SearcherLevenshteinMetricSettings:
        return SearcherLevenshteinMetricSettings(
            self._raw_settings['obfuscation']['searcher_by_levenshtein_metric'])

    @property
    def word_loader_settings(self) -> WordLoaderSettings:
        return WordLoaderSettings(self._raw_settings['word_loader'])
