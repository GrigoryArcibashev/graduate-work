from enum import Enum


class DangerLevel(Enum):
    DANGEROUS = 0
    SUSPICIOUS = 1
    PAY_ATTENTION = 2


class SuspiciousType(Enum):
    GENERAL = 0  # 'Подозрительная лексема'
    COMMAND = 1  # 'Команды bash/cmd'
    ENCRYPT = 2  # '[Де]шифрование'
    EXECUTION = 3  # 'Вычисление переданного выражения'
    FILES = 4  # 'Взаимодействие с файлами'
    IMPORT = 5  # 'Подключение внешних скриптов/библиотек'
    NET = 6  # 'Загрузка/отправка файлов по сети'
    OS = 7  # 'Взаимодействие с функциями ОС'
