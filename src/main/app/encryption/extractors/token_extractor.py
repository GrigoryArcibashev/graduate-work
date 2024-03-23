from collections import namedtuple
from enum import Enum
from typing import Iterator

Token = namedtuple('Token', ['value', 'type'])


class TokenType(Enum):
    LETTERS = 0
    DIGITS = 1
    OTHER = 2


class TokenExtractor:
    def get_token_iter(self, string) -> Iterator[Token]:
        current_lexeme = list()
        symbol_type = None
        prev_symbol_type = None
        for i in range(len(string)):
            symbol = string[i]
            symbol_type = self._determinate_type(symbol)
            if self._is_new_lexeme(prev_symbol_type, symbol, symbol_type):
                yield Token(current_lexeme, prev_symbol_type)
                current_lexeme = []
            current_lexeme.append(symbol)
            prev_symbol_type = symbol_type
        if current_lexeme:
            yield Token(current_lexeme, symbol_type)

    def _is_new_lexeme(self, prev_symbol_type, symbol, symbol_type) -> bool:
        return prev_symbol_type and (symbol_type != prev_symbol_type or self._is_non_alphanum(symbol))

    def _determinate_type(self, symbol) -> TokenType:
        if self._is_letter(symbol):
            return TokenType.LETTERS
        if self._is_digit(symbol):
            return TokenType.DIGITS
        return TokenType.OTHER

    def _is_non_alphanum(self, symbol) -> bool:
        return not (self._is_letter(symbol) or self._is_digit(symbol))

    @staticmethod
    def _is_letter(symbol) -> bool:
        return (
                ord(b'a') <= symbol <= ord(b'z')
                or ord(b'A') <= symbol <= ord(b'Z')
        )

    @staticmethod
    def _is_digit(symbol) -> bool:
        return ord(b'0') <= symbol <= ord(b'9')