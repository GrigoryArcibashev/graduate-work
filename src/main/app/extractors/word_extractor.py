from typing import Iterator

from src.main.app.extractors.word import Word


class WordExtractor:
    def __init__(self):
        self._case_distance = ord('a') - ord('A')

    def get_word_iter(self, string) -> Iterator[Word]:
        current_lexeme = list()
        prev_symbol = None
        for i in range(len(string)):
            symbol = string[i]
            if self.is_new_lexeme(prev_symbol, symbol):
                yield Word(self._to_lower(current_lexeme))
                current_lexeme = []
            current_lexeme.append(symbol)
            prev_symbol = symbol
        if current_lexeme:
            yield Word(self._to_lower(current_lexeme))

    def is_new_lexeme(self, prev_symbol: int, symbol: int) -> bool:
        """
        TRUE: aA
        FALSE: a A aa Aa AA
        """
        if not prev_symbol:
            return False
        return not self._is_upper_letter(prev_symbol) and self._is_upper_letter(symbol)

    @staticmethod
    def _is_upper_letter(symbol: int) -> bool:
        return ord(b'A') <= symbol <= ord(b'Z')

    def _to_lower(self, lexeme: list[int]) -> list[int]:
        return [c + self._case_distance if self._is_upper_letter(c) else c for c in lexeme]
