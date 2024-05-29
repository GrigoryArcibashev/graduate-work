from enum import Enum


class DangerLevel(Enum):
    DANGEROUS = 0
    SUSPICIOUS = 1
    PAY_ATTENTION = 2


class SuspiciousType(Enum):
    GENERAL = 0
    COMMAND = 1
    ENCRYPT = 2
    EXECUTION = 3
    FILES = 4
    IMPORT = 5
    NET = 6
    OS = 7
