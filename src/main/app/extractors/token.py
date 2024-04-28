from enum import Enum
from typing import Iterable


class TokenType(Enum):
    LETTERS = 0
    DIGITS = 1
    UNDERLINING = 2
    OTHER = 3


class Token:
    """
    Единица информации о последовательности символов
    """

    def __init__(self, value: Iterable[int], token_type: TokenType):
        self.__value = tuple(value)
        self.__type = token_type

    @property
    def value(self) -> tuple[int]:
        return self.__value

    @property
    def type(self) -> TokenType:
        return self.__type

    def __hash__(self):
        return hash((self.__value, self.__type))

    def __eq__(self, other):
        if not isinstance(other, Token):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
        return self.value == other.value and self.type == other.type

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return f'type = {self.type}, val = {self.value} ({repr(self._numbers_of_bytes_to_str(self.value))})'

    def __repr__(self):
        return f'\'{self.__str__()}\''

    @staticmethod
    def _numbers_of_bytes_to_str(numbers: tuple[int]) -> str:
        return ''.join(tuple(map(chr, numbers)))
