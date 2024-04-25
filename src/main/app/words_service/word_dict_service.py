from typing import Optional

from src.main.app.words_service.word_loader import AbstractWordLoader
from src.main.app.extractors.word import Word


class WordDictService:
    """
    Сервис для работы со словарем слов
    """

    def __init__(self, word_loader: AbstractWordLoader):
        self._words_by_len = word_loader.load()
        self._min_len = min(self._words_by_len.keys())
        self._max_len = max(self._words_by_len.keys())

    def check_word(self, word: Word) -> bool:
        """
        Проверяет наличие слова в словаре
        :param word: проверяемое слово
        :return: True, если слово найдено, иначе - False
        """
        return len(word) in self._words_by_len and word in self._words_by_len[len(word)]

    def get_words_with_len(self, length: int) -> Optional[set[Word]]:
        """
        Возвращает множество всех слов в словаре длины length
        :param length: требуемая длина слов

        :return: множество всех слов длины length, если слов такой длины нет - None
        """
        return self._words_by_len.get(length)

    def get_min_len(self) -> int:
        """
        :return: длина наикратчайшего слова в словаре
        """
        return self._min_len

    def get_max_len(self) -> int:
        """
        :return: длина наидлиннейшего слова в словаре
        """
        return self._max_len
