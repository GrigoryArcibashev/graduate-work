from enum import Enum


class DangerLevel(Enum):
    DANGEROUS = 0
    SUSPICIOUS = 1
    PAY_ATTENTION = 2

    def to_str(self) -> str:
        if self == DangerLevel.DANGEROUS:
            return 'опасный'
        if self == DangerLevel.SUSPICIOUS:
            return 'подозрительный'
        if self == DangerLevel.PAY_ATTENTION:
            return 'требует проверки'

    def __str__(self):
        return self.to_str()


class SuspiciousType(Enum):
    GENERAL = 0
    COMMAND = 1
    ENCRYPT = 2
    EXECUTION = 3
    FILES = 4
    IMPORT = 5
    NET = 6
    OS = 7

    def to_str(self) -> str:
        if self == SuspiciousType.GENERAL:
            return 'общее'
        if self == SuspiciousType.COMMAND:
            return 'команда оболочки ОС'
        if self == SuspiciousType.ENCRYPT:
            return 'преобразование'
        if self == SuspiciousType.EXECUTION:
            return 'выполнение кода'
        if self == SuspiciousType.FILES:
            return 'работа с ФС'
        if self == SuspiciousType.IMPORT:
            return 'подключение модулей'
        if self == SuspiciousType.NET:
            return 'работа с сетью'
        if self == SuspiciousType.OS:
            return 'работа с функциями ОС'

    def __str__(self):
        return self.to_str()
