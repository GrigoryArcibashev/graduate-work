import re

from src.main.app.encryption.encryption_determinator.encryption_determinants.abstract_encryption_determinator import \
    AbstractEncryptionDeterminator
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode, EncrVerdict


class EncryptionDeterminatorByHEX(AbstractEncryptionDeterminator):
    """
    Обнаруживает HEX в тексте
    """

    def __init__(self, mode: OperatingMode):
        super().__init__()
        self._min_count = None
        self.mode = mode
        self._pattern = re.compile(br'(?:\\x|0x|\\u)[0-9abcdef]{2}', re.IGNORECASE)
        self._unicode_markers = [
            (br'\xef', br'\xbb', br'\xbf'),  # UTF8
            (br'0xef', br'0xbb', br'0xbf'),
            (br'\xff', br'\xfe'),  # UTF16 LE
            (br'0xff', br'0xfe'),
            (br'\xfe', br'\xff'),  # UTF16 BE
            (br'0xfe', br'0xff'),
            (br'\xff', br'\xfe', br'\x00', br'\x00'),  # UTF32 LE
            (br'0xff', br'0xfe', br'0x00', br'0x00'),
            (br'\x00', br'\x00', br'\xfe', br'\xff'),  # UTF32 BE
            (br'0x00', br'0x00', br'0xfe', br'0xff'),
            (br'\x2b', br'\x2f', br'\x76', br'\x38'),  # UTF7 (1)
            (br'0x2b', br'0x2f', br'0x76', br'0x38'),
            (br'\x2b', br'\x2f', br'\x76', br'\x39'),  # UTF7 (2)
            (br'0x2b', br'0x2f', br'0x76', br'0x39'),
            (br'\x2b', br'\x2f', br'\x76', br'\x2b'),  # UTF7 (3)
            (br'0x2b', br'0x2f', br'0x76', br'0x2b'),
            (br'\x2b', br'\x2f', br'\x76', br'\x2f'),  # UTF7 (4)
            (br'0x2b', br'0x2f', br'0x76', br'0x2f'),
            (br'\xf7', br'\x64', br'\x4c'),  # UTF1
            (br'0xf7', br'0x64', br'0x4c'),
            (br'\xdd', br'\x73', br'\x66', br'\x73'),  # UTF-EBCDIC
            (br'0xdd', br'0x73', br'0x66', br'0x73')
        ]

    def _set_boundaries(self, mode: OperatingMode) -> None:
        """
        Устанавливает граничные параметры для определения шифра,
        основываясь на режиме работы определителя

        :param mode: режим работы определителя

        :return: None
        """
        self._min_count = 3 if mode.is_strict else 10

    def determinate(self, data: bytes) -> EncrVerdict:
        """
        Определяет наличие шифра в тексте

        :param data: текст
        :return: вердикт (EncrVerdict)
        """
        found = re.findall(self._pattern, data)
        count = len(self._filter_unicode(found))
        return EncrVerdict.DETECTED if count > self._min_count else EncrVerdict.NOT_DETECTED

    def _filter_unicode(self, found) -> list:
        """
        Удаляет маркеры кодировок из найденного hex

        :param found: hex
        :return: hex без маркеров кодировок
        """
        for marker in self._unicode_markers:
            len_mkr = len(marker)
            if len_mkr <= len(found) and self._hex_eq(marker, found[:len_mkr]):
                return found[len_mkr:]
        return found

    @staticmethod
    def _hex_eq(hex1, hex2) -> bool:
        """
        (Вспомогательный метод)

        Проверяет равенство hex-ов

        :param hex1: первый hex
        :param hex2: второй hex
        :return: равны => True, нет => False
        """
        if len(hex1) != len(hex2):
            return False
        for i in range(len(hex1)):
            if hex1[i].lower() != hex2[i].lower():
                return False
        return True
