from typing import Iterator, Optional

from src.main.app.extractors.word import Word


class WordExtractor:
    """
    Извлекает слова из последовательности символов в виде их номеров
    """

    def __init__(self):
        self._case_distance = ord('a') - ord('A')

    def get_word_iter(self, string: tuple[int]) -> Iterator[Word]:
        """
        Возвращает итератор по всем словам в string

        :param string: последовательность символов в виде их номеров

        :return: итератор по словам (Word)
        """
        current_lexeme = list()
        prev_symbol = None
        for i in range(len(string)):
            symbol = string[i]
            if self.is_new_word(prev_symbol, symbol):
                yield Word(self._to_lower(current_lexeme))
                current_lexeme = []
            current_lexeme.append(symbol)
            prev_symbol = symbol
        if current_lexeme:
            yield Word(self._to_lower(current_lexeme))

    def is_new_word(self, prev_symbol: Optional[int], symbol: int) -> bool:
        """
        Определяет по предыдущему и текущему символам, началось ли новое слово

        True: aA

        False: a A aa Aa AA

        :param prev_symbol: номер предыдущего прочтенного символа
        :param symbol: номер текущего символа
        :return: True, если обнаружено новое слово, иначе - False
        """

        if not prev_symbol:
            return False
        return not self._is_upper_letter(prev_symbol) and self._is_upper_letter(symbol)

    @staticmethod
    def _is_upper_letter(symbol: int) -> bool:
        """
        Проверяет, является ли номер номером буквы в верхнем регистре

        :param symbol: номер символа

        :return: True, если это номер буквы в верхнем регистре, иначе - False
        """
        return ord(b'A') <= symbol <= ord(b'Z')

    def _to_lower(self, word: list[int]) -> list[int]:
        """
        Переводит все символы верхнего регистра в нижний

        :param word: последовательность символов в виде их номеров

        :return: последовательность в нижнем регистре
        """
        return [let + self._case_distance if self._is_upper_letter(let) else let for let in word]
