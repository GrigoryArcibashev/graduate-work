from typing import Iterator

from src.main.app.model.extractors.token import Token, TokenType


class TokenExtractor:
    """
    Формирует последовательность токенов
    """

    def get_token_iter(self, data: list[int]) -> Iterator[Token]:
        """
        Возвращает итератор по токенам, полученных из текста

        :param data: текст в виде последовательности номеров байт

        :return: итератор по токенам
        """
        current_lexeme = list()
        symbol_type = None
        prev_symbol_type = None
        for i in range(len(data)):
            symbol = data[i]
            symbol_type = self._determinate_type(symbol)
            if self._is_new_lexeme(prev_symbol_type, symbol, symbol_type):
                yield Token(current_lexeme, prev_symbol_type)
                current_lexeme = []
            current_lexeme.append(symbol)
            prev_symbol_type = symbol_type
        if current_lexeme:
            yield Token(current_lexeme, symbol_type)

    def _is_new_lexeme(self, prev_symbol_type: TokenType, symbol: int, symbol_type: TokenType) -> bool:
        """
        Определяет, началась ли новая лексема (=новый токен)

        Например, буквы -> цифры

        :param prev_symbol_type: тип предыдущего символа
        :param symbol: текущий символ (номер байта)
        :param symbol_type: тип текущего символа
        :return: True, если началась новая лексема, иначе - False
        """
        return prev_symbol_type and (symbol_type != prev_symbol_type or not self._is_alphanum(symbol))

    def _determinate_type(self, symbol: int) -> TokenType:
        """
        Определяет тип символа

        :param symbol: символ (номер байта)
        :return: тип символа
        """
        if self._is_letter(symbol):
            return TokenType.LETTERS
        if self._is_digit(symbol):
            return TokenType.DIGITS
        if self._is_underlining(symbol):
            return TokenType.UNDERLINING
        return TokenType.OTHER

    def _is_alphanum(self, symbol: int) -> bool:
        """
        Является ли символ цифрой или буквой

        :param symbol: символ (номер байта)
        :return: True / False
        """
        return self._is_letter(symbol) or self._is_digit(symbol)

    @staticmethod
    def _is_letter(symbol: int) -> bool:
        """
        Является ли символ буквой

        :param symbol: символ (номер байта)
        :return: True / False
        """
        return (
                ord(b'a') <= symbol <= ord(b'z')
                or ord(b'A') <= symbol <= ord(b'Z')
        )

    @staticmethod
    def _is_digit(symbol: int) -> bool:
        """
        Является ли символ цифрой

        :param symbol: символ (номер байта)
        :return: True / False
        """
        return ord(b'0') <= symbol <= ord(b'9')

    @staticmethod
    def _is_underlining(symbol: int) -> bool:
        """
        Является ли символ символом нижнего подчеркивания

        :param symbol: символ (номер байта)
        :return: True / False
        """
        return symbol == ord(b'_')
