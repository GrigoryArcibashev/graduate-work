from typing import Iterable


class Word:
    """
    Класс-обёртка над словом
    """

    def __init__(self, value: Iterable):
        self.__value = tuple(value)

    @property
    def value(self) -> tuple[int]:
        return self.__value

    def __str__(self):
        return f'{self.value} ({repr(self._numbers_of_bytes_to_str(self.value))})'

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        return hash(self.__value)

    def __eq__(self, other):
        if other is None or not isinstance(other, Word):
            return False
        return self.value == other.value

    @staticmethod
    def _numbers_of_bytes_to_str(numbers: tuple[int]) -> str:
        return ''.join(tuple(map(chr, numbers)))
