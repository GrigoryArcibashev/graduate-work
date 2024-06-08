from src.main.app.model.settings.analyzer_settings import AnalyzerSettings
from src.main.app.model.settings.db_settings import DBSettings
from src.main.app.model.settings.hash_settings import HashSettings
from src.main.app.model.file_service.file_reader import FileReader


class Settings:
    def __init__(self, raw_settings: dict):
        self._raw_settings = raw_settings

    @property
    def hasher_settings(self) -> HashSettings:
        return HashSettings(self._raw_settings['hash'])

    @property
    def database_settings(self) -> DBSettings:
        return DBSettings(self._raw_settings['database'])

    @property
    def analyzer_settings(self) -> AnalyzerSettings:
        return AnalyzerSettings(self._raw_settings)
