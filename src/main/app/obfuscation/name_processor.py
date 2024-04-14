from typing import Iterator

from src.main.app.encryption.extractors.token_extractor import TokenType
from src.main.app.encryption.extractors.word_extractor import WordExtractor, Word
from src.main.app.obfuscation.searchers.name import Name
from src.main.app.obfuscation.searchers.searchers import AbstractSearcher


class NameInfo:
    def __init__(self, words: list[Word], name_len: int, digit_len: int):
        self._words = words
        self._name_len = name_len
        self._digit_len = digit_len

    @property
    def words(self) -> list[Word]:
        return self._words

    @property
    def name_len(self) -> int:
        return self._name_len

    @property
    def digit_len(self) -> int:
        return self._digit_len


class NameProcessor:
    def __init__(self, searchers: list[AbstractSearcher], word_extractor: WordExtractor):
        self._searchers = searchers
        self._word_extractor = word_extractor

    def get_next_name_info(self, text) -> Iterator[NameInfo]:
        for searcher in self._searchers:
            for name in searcher.get_name_iter(text):
                yield self._make_name_info(name)

    def _make_name_info(self, name: Name) -> NameInfo:
        words = list()
        name_len = digit_len = 0
        for token in name.value:
            name_len += len(token)
            if token.type == TokenType.LETTERS:
                words.extend(list(self._word_extractor.get_word_iter(token.value)))
            else:
                digit_len += len(token)
        return NameInfo(words, name_len, digit_len)
