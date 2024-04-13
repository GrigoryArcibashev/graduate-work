from abc import abstractmethod
from enum import Enum
from typing import Iterator

from src.main.app.encryption.extractors.token_extractor import TokenExtractor, TokenType, Token


class Language(Enum):
    PHP = 0
    JS = 1
    PYTHON_RUBY = 2
    C_SHARP = 3


class Name:
    def __init__(self, value: list[Token], lang: Language):
        self._value = value
        self._lang = lang

    @property
    def value(self) -> list[Token]:
        return self._value

    @property
    def lang(self) -> Language:
        return self._lang


class Searcher:
    def __init__(self, token_extractor: TokenExtractor):
        self._token_extractor = token_extractor

    @abstractmethod
    def get_name_iter(self, string) -> Iterator[Name]:
        pass

    def _extract_names(self, raw_str) -> Iterator[list[Token]]:
        current_name = list()
        for token in self._token_extractor.get_token_iter(list(raw_str)):
            if token.type == TokenType.LETTERS or token.type == TokenType.DIGITS:
                current_name.append(token)
            elif current_name:
                yield current_name
                current_name.clear()
        if current_name:
            yield current_name
