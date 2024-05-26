class WordLoaderSettings:
    def __init__(self, raw_settings: dict):
        self._path_to_word_dict = str(raw_settings['path_to_word_dict'])

    @property
    def path_to_word_dict(self) -> str:
        return self._path_to_word_dict
