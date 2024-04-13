from enum import Enum
from typing import Iterator


class TokenType(Enum):
    LETTERS = 0
    DIGITS = 1
    UNDERLINING = 2
    OTHER = 3


class Token:
    def __init__(self, value, token_type: TokenType):
        self.__value = tuple(value)
        self.__type = token_type

    @property
    def value(self) -> tuple:
        return self.__value

    @property
    def type(self) -> TokenType:
        return self.__type

    def __hash__(self):
        return hash((self.__value, self.__type))

    def __len__(self):
        return len(self.value)

    def __eq__(self, other):
        if not isinstance(other, Token):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
        return self.value == other.value and self.type == other.type

    def __str__(self):
        return f'type = {self.type}, val = {self.value} ({repr(self._numbers_of_bytes_to_str(self.value))})'

    def __repr__(self):
        return f'\'{self.__str__()}\''

    @staticmethod
    def _numbers_of_bytes_to_str(numbers: list[int]) -> str:
        return ''.join(tuple(map(chr, numbers)))


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
        if self._is_underlining(symbol):
            return TokenType.UNDERLINING
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

    @staticmethod
    def _is_underlining(symbol) -> bool:
        return symbol == ord(b'_')
