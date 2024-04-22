from enum import Enum


class DangerLevel(Enum):
    DANGEROUS = 0
    SUSPICIOUS = 1
    PAY_ATTENTION = 2


class SuspiciousType(Enum):
    GENERAL = 'Подозрительная лексема'
    COMMAND = 'Команды bash/cmd'
    ENCRYPT = '[Де]шифрование'
    EXECUTION = 'Вычисление переданного выражения'
    FILES = 'Взаимодействие с файлами'
    IMPORT = 'Подключение внешних скриптов/библиотек'
    NET = 'Загрузка/отправка файлов по сети'
    OS = 'Взаимодействие с функциями ОС'
