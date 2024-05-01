import re

from src.main.app.encryption.encryption_determinator.encryption_determinants.abstract_encryption_determinator import \
    AbstractEncryptionDeterminator
from src.main.app.encryption.encryption_determinator.encryption_determinants.encr_determinator_hex.code_markers import \
    MARKERS
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode, EncrVerdict


class EncryptionDeterminatorByHEX(AbstractEncryptionDeterminator):
    """
    Обнаруживает HEX в тексте
    """

    def __init__(self, mode: OperatingMode):
        super().__init__()
        self._min_count_optimal = 3
        self._min_count_strict = 10
        self.mode = mode
        self._pattern = re.compile(br'(?:\\x|0x|\\u)[0-9abcdef]{2}', re.IGNORECASE)
        self._markers = MARKERS

    def determinate(self, data: bytes) -> EncrVerdict:
        """
        Определяет наличие шифра в тексте

        :param data: текст
        :return: вердикт (EncrVerdict)
        """
        found = re.findall(self._pattern, data)
        count = len(self._filter_unicode(found))
        return EncrVerdict.DETECTED if count > self._min_count else EncrVerdict.NOT_DETECTED

    @property
    def _min_count(self) -> int:
        """
        Устанавливает граничный параметр для обнаружения шифра,
        основываясь на режиме работы определителя

        :return: граничный параметр
        """
        return self._min_count_strict if self.mode.is_strict else self._min_count_optimal

    def _filter_unicode(self, found) -> list:
        """
        Удаляет маркеры кодировок из найденного hex

        :param found: hex
        :return: hex без маркеров кодировок
        """
        for marker in self._markers:
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
