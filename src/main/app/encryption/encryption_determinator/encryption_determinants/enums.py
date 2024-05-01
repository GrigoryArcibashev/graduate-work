from enum import Enum


class OperatingMode(Enum):
    """
    Режимы работы определителя шифра
    """
    OPTIMAL = 0
    STRICT = 1

    @property
    def is_strict(self) -> bool:
        return self == OperatingMode.STRICT


class EncrVerdict(Enum):
    """
    Вердикт определителя шифра:
    крайне вероятно / вероятно / маловероятно,
    что зашифрован
    """
    DETECTED = 0
    NOT_DETECTED = 1

    def __str__(self):
        return self.to_str()

    def to_str(self) -> str:
        if self == EncrVerdict.DETECTED:
            return 'ОБНАРУЖЕН'
        else:
            return 'НЕ ОБНАРУЖЕН'

    @property
    def is_encr(self) -> bool:
        return self != EncrVerdict.NOT_DETECTED
