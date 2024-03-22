from src.main.app.encryption.encr_filter.words.word_provider import WordProvider
from src.main.app.encryption.extractors.token_extractor import TokenExtractor
from src.main.app.encryption.extractors.word_extractor import WordExtractor


class EncryptionFilter:
    def __init__(self, word_provider: WordProvider):
        self._word_provider = word_provider
        self._token_extractor = TokenExtractor()
        self._word_extractor = WordExtractor()

    def filter(self, data: list[int]) -> list[int]:
        self._token_extractor.get_token_iter(data)
        while
        result = list()

        return result
