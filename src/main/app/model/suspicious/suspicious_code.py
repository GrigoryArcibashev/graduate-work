from typing import Union

from src.main.app.model.suspicious.enums import DangerLevel, SuspiciousType


class SuspiciousCode:
    def __init__(self, code: Union[str, bytes], danger_lvl: DangerLevel, suspy_type: SuspiciousType):
        self.__code = code if isinstance(code, bytes) else code.encode()
        self.__lvl = danger_lvl
        self.__type = suspy_type

    @property
    def code(self) -> bytes:
        return self.__code

    @property
    def code_as_str(self) -> str:
        return self.code.decode()

    @property
    def type(self) -> SuspiciousType:
        return self.__type

    @property
    def danger_lvl(self) -> DangerLevel:
        return self.__lvl

    def __hash__(self):
        return hash((self.__code, self.__type, self.__lvl))

    def __eq__(self, other):
        if other is None or not isinstance(other, SuspiciousCode):
            return False
        return self.code == other.code and self.type == other.type and self.danger_lvl == other.danger_lvl

    def __str__(self):
        return f'{self.danger_lvl} => {self.type} => {self.code}'
