from src.main.app.settings.calculator_levenshtein_metric_settings import CalculatorLevenshteinMetricSettings
from src.main.app.settings.encr_entropy_settings import EncrDetEntropySettings
from src.main.app.settings.encr_filter_settings import EncrFilterSettings
from src.main.app.settings.encr_hex_settings import EncrDetHEXSettings
from src.main.app.settings.entropy_analyzer_settings import EntropyAnalyzerSettings
from src.main.app.settings.obfuscation_determinator_settings import ObfuscationDetSettings
from src.main.app.settings.searcher_levenshtein_metric_settings import SearcherLevenshteinMetricSettings


class Settings:
    def __init__(self):
        pass

    @property
    def encr_determinator_entropy_settings(self) -> EncrDetEntropySettings:
        pass

    @property
    def encr_determinator_hex_settings(self) -> EncrDetHEXSettings:
        pass

    @property
    def encr_filter_settings(self) -> EncrFilterSettings:
        pass

    @property
    def entropy_analyzer_settings(self) -> EntropyAnalyzerSettings:
        pass

    @property
    def obf_determinator_settings(self) -> ObfuscationDetSettings:
        pass

    @property
    def calc_levenshtein_metric_settings(self) -> CalculatorLevenshteinMetricSettings:
        pass

    @property
    def searcher_levenshtein_metric_settings(self) -> SearcherLevenshteinMetricSettings:
        pass
