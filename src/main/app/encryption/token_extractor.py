from enum import Enum
from collections import namedtuple

Token = namedtuple('Token', ['value', 'type'])


class TokenType(Enum):
    LETTERS = 0
    DIGITS = 1
    TERMINATOR = 2
    OTHER = 3


class TokenExtractor:
    def __init__(self):
        self._terminator = ord(b'_')

    def extract_tokens_from_string(self, string):
        """
        extract by camelCase, snake_case, terminator and non alphanum symbols
        :param string: string
        :return: all tokens in the string
        """
        tokens = list()
        current_lexeme = list()
        symbol_type = None
        prev_symbol_type = None
        for i in range(len(string)):
            symbol = string[i]
            symbol_type = self._determinate_type(symbol)
            if self._is_new_lexeme(prev_symbol_type, symbol, symbol_type):
                tokens.append(Token(current_lexeme, prev_symbol_type))
                current_lexeme = []
            current_lexeme.append(symbol)
            prev_symbol_type = symbol_type
        if current_lexeme:
            tokens.append(Token(current_lexeme, symbol_type))
        return tokens

    def _is_new_lexeme(self, prev_symbol_type, symbol, symbol_type):
        return prev_symbol_type and (
                symbol_type != prev_symbol_type or
                self._is_upper_letter(symbol) or
                self._is_non_alphanum(symbol)
        )

    def _determinate_type(self, symbol: bytes):
        if self._is_letter(symbol):
            return TokenType.LETTERS
        if self._is_digit(symbol):
            return TokenType.DIGITS
        if self._is_terminator(symbol):
            return TokenType.TERMINATOR
        return TokenType.OTHER

    def _is_terminator(self, symbol):
        return symbol == self._terminator

    def _is_non_alphanum(self, symbol):
        return not (self._is_letter(symbol) or self._is_digit(symbol))

    @staticmethod
    def _is_letter(symbol):
        return (
                ord(b'a') <= symbol <= ord(b'z')
                or ord(b'A') <= symbol <= ord(b'Z')
        )

    @staticmethod
    def _is_upper_letter(symbol):
        return ord(b'A') <= symbol <= ord(b'Z')

    @staticmethod
    def _is_digit(symbol):
        return ord(b'0') <= symbol <= ord(b'9')
