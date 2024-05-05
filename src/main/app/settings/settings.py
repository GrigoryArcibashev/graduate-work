from src.main.app.settings.calculator_levenshtein_metric_settings import CalculatorLevenshteinMetricSettings
from src.main.app.settings.encr_entropy_settings import EncrDetEntropySettings
from src.main.app.settings.encr_filter_settings import EncrFilterSettings
from src.main.app.settings.encr_hex_settings import EncrDetHEXSettings
from src.main.app.settings.entropy_analyzer_settings import EntropyAnalyzerSettings
from src.main.app.settings.obfuscation_determinator_settings import ObfuscationDetSettings
from src.main.app.settings.searcher_levenshtein_metric_settings import SearcherLevenshteinMetricSettings
from src.main.app.settings.word_loader_settings import WordLoaderSettings
from src.main.app.util.file_reader import read_json


class Settings:
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

    @property
    def word_loader_settings(self) -> WordLoaderSettings:
        pass


if __name__ == '__main__':
    sts = Settings(read_json('../../settings.json'))
    entr_ = sts.encr_determinator_entropy_settings
    hex_ = sts.encr_determinator_hex_settings
    print()
