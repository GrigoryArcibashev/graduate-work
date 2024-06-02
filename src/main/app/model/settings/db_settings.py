class DBSettings:
    def __init__(self, raw_settings: dict):
        self._path_to_database = str(raw_settings['path_to_db'])

    @property
    def path_to_database(self) -> str:
        return self._path_to_database
