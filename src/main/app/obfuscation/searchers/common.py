from abc import abstractmethod
from re import Pattern
from typing import Iterator

from src.main.app.encryption.extractors.token_extractor import TokenExtractor, TokenType, Token


class Name:
    def __init__(self, value: tuple[Token]):
        self.__value = tuple(value)

    @property
    def value(self) -> tuple[Token]:
        return self.__value

    def __hash__(self):
        return hash(self.__value)

    def __eq__(self, other):
        if not isinstance(other, Name):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
        return self.value == other.value


class Searcher:
    def __init__(self, token_extractor: TokenExtractor):
        self._token_extractor = token_extractor

    @property
    @abstractmethod
    def patterns(self) -> tuple[Pattern]:
        pass

    def get_name_iter(self, string) -> Iterator[Name]:
        for pattern in self.patterns:
            found = pattern.findall(string)
            if not found:
                continue
            for group_num in range(len(found)):
                for match in self.__wrap_in_tuple_if_necessary(found[group_num]):
                    if not match:
                        continue
                    for name in self._extract_names(match):
                        yield Name(value=name)

    @staticmethod
    def __wrap_in_tuple_if_necessary(group):
        if not isinstance(group, tuple):
            return (group,)
        return group

    def _extract_names(self, raw_str) -> Iterator[tuple[Token]]:
        current_name = list()
        for token in self._token_extractor.get_token_iter(list(raw_str)):
            if token.type == TokenType.LETTERS or token.type == TokenType.DIGITS:
                current_name.append(token)
            elif current_name and token.type != TokenType.UNDERLINING:
                yield tuple(current_name)
                current_name.clear()
        if current_name:
            yield tuple(current_name)
