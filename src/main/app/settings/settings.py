from src.main.app.settings.analyzer_settings import AnalyzerSettings
from src.main.app.settings.hash_settings import HashSettings
from src.main.app.file_service.file_reader import FileReader


class Settings:
    def __init__(self, raw_settings: dict):
        self._raw_settings = raw_settings

    @property
    def hasher_settings(self) -> HashSettings:
        return HashSettings(self._raw_settings['hash'])

    @property
    def analyzer_settings(self) -> AnalyzerSettings:
        return AnalyzerSettings(self._raw_settings)


if __name__ == '__main__':
    sts = Settings(FileReader.read_json('../../settings.json'))
    settings = sts.analyzer_settings
    print()
