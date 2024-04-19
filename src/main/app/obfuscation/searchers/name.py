from src.main.app.encryption.extractors.token_extractor import Token


class Name:
    def __init__(self, value: tuple[Token]):
        self.__value = tuple(value)

    @property
    def value(self) -> tuple[Token]:
        return self.__value

    def __hash__(self):
        return hash(self.__value)

    def __eq__(self, other):
        if not isinstance(other, Name):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
        return self.value == other.value
