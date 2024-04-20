from typing import Iterator

from src.main.app.extractors.word import Word


class WordExtractor:
    def get_word_iter(self, string) -> Iterator[Word]:
        current_lexeme = list()
        prev_symbol = None
        for i in range(len(string)):
            symbol = string[i]
            if self.is_new_lexeme(prev_symbol, symbol):
                yield Word(current_lexeme)
                current_lexeme = []
            current_lexeme.append(symbol)
            prev_symbol = symbol
        if current_lexeme:
            yield Word(current_lexeme)

    def is_new_lexeme(self, prev_symbol, symbol) -> bool:
        """
        TRUE: aA
        FALSE: a A aa Aa AA
        """
        if not prev_symbol:
            return False
        return not self._is_upper_letter(prev_symbol) and self._is_upper_letter(symbol)

    @staticmethod
    def _is_upper_letter(symbol) -> bool:
        return ord(b'A') <= symbol <= ord(b'Z')
