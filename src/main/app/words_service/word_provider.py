from src.main.app.words_service.word_loader import AbstractWordLoader
from src.main.app.extractors.word import Word


class WordProvider:
    def __init__(self, word_loader: AbstractWordLoader):
        self._words_by_len = word_loader.load()
        self._min_len = min(self._words_by_len.keys())
        self._max_len = max(self._words_by_len.keys())

    def check_word(self, word: Word) -> bool:
        return len(word) in self._words_by_len and word in self._words_by_len[len(word)]

    def get_words_with_len(self, length: int):
        return self._words_by_len.get(length)

    def get_min_len(self) -> int:
        return self._min_len

    def get_max_len(self) -> int:
        return self._max_len
