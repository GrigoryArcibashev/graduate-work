from enum import Enum


class OperatingMode(Enum):
    OPTIMAL = 0
    STRICT = 1


class EncrVerdict(Enum):
    EXTREMELY_LIKELY = 0
    LIKELY = 1
    UNLIKELY = 2

    def __str__(self):
        return self.to_str()

    def to_str(self) -> str:
        if self == EncrVerdict.EXTREMELY_LIKELY:
            return 'КРАЙНЕ ВЕРОЯТНО'
        if self == EncrVerdict.LIKELY:
            return 'ВЕРОЯТНО'
        if self == EncrVerdict.UNLIKELY:
            return 'НЕТ'

    @property
    def is_encr(self) -> bool:
        return self != EncrVerdict.UNLIKELY
