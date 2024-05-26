from src.main.app.model.extractors.token import Token


class Name:
    def __init__(self, value: tuple[Token]):
        self.__value = tuple(value)

    @property
    def value(self) -> tuple[Token]:
        return self.__value

    def __hash__(self):
        return hash(self.__value)

    def __eq__(self, other):
        if other is None or not isinstance(other, Name):
            return False
        return self.value == other.value
