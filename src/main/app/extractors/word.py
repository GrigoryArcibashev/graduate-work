class Word:
    def __init__(self, value):
        self.__value = tuple(value)

    def __str__(self):
        return f'{self.value} ({repr(self._numbers_of_bytes_to_str(self.value))})'

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        return hash(self.__value)

    def __eq__(self, other):
        if not isinstance(other, Word):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
        return self.value == other.value

    @property
    def value(self) -> tuple[int]:
        return self.__value

    @staticmethod
    def _numbers_of_bytes_to_str(numbers: tuple[int]) -> str:
        return ''.join(tuple(map(chr, numbers)))
