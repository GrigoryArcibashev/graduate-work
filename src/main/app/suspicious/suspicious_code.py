from src.main.app.suspicious.enums import DangerLevel, SuspiciousType


class SuspiciousCode:
    def __init__(self, code: bytes, danger_lvl: DangerLevel, code_type: SuspiciousType):
        self.__code = code
        self.__lvl = danger_lvl
        self.__type = code_type

    @property
    def code(self) -> bytes:
        return self.__code

    @property
    def type(self) -> SuspiciousType:
        return self.__type

    @property
    def danger_lvl(self) -> DangerLevel:
        return self.__lvl

    def __hash__(self):
        return hash((self.__code, self.__type, self.__lvl))

    def __eq__(self, other):
        if not isinstance(other, SuspiciousCode):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
        return self.code == other.code and self.type == other.type and self.danger_lvl == other.danger_lvl

    def __str__(self):
        return f'{self.danger_lvl} => {self.type} => {self.code}'
