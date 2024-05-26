import re
from typing import Iterator

from src.main.app.model.encryption.encryption_determinator.encryption_determinants.abstract_encryption_determinator import \
    AbstractEncryptionDeterminator
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.encr_determinator_hex.code_markers import \
    MARKERS
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import EncrVerdict
from src.main.app.model.settings.encr_hex_settings import EncrDetHEXSettings


class EncryptionDeterminatorByHEX(AbstractEncryptionDeterminator):
    """
    Обнаруживает HEX в тексте
    """

    def __init__(self, settings: EncrDetHEXSettings):
        super().__init__()
        self._min_count_optimal = settings.min_count_optimal
        self._min_count_strict = settings.min_count_strict
        self.mode = settings.mode
        self._pattern = re.compile(br'(?:\\x|0x|\\u)[0-9abcdef]{2}', re.IGNORECASE)
        self._markers = MARKERS

    def determinate_by_iter(self, data_iter: Iterator[bytes]) -> EncrVerdict:
        """
        Определяет наличие шифра в тексте

        :param data_iter: итератор по тексту
        :return: вердикт (EncrVerdict)
        """
        count = sum([self._calc_number_of_pat_match(data) for data in data_iter])
        return self._make_verdict(count)

    def determinate(self, data: bytes) -> EncrVerdict:
        """
        Определяет наличие шифра в тексте

        :param data: текст
        :return: вердикт (EncrVerdict)
        """
        count = self._calc_number_of_pat_match(data)
        return self._make_verdict(count)

    def _make_verdict(self, count: int) -> EncrVerdict:
        """
        Выносит вердикт

        :param count: сколько раз встречается паттерн в data
        :return: вердикт
        """
        return EncrVerdict.DETECTED if count > self._min_count else EncrVerdict.NOT_DETECTED

    def _calc_number_of_pat_match(self, data: bytes) -> int:
        """
        Считает, сколько раз встречается паттерн в data

        :param data: текст
        :return: сколько раз встречается паттерн в data
        """
        found = re.findall(self._pattern, data)
        return len(self._filter_unicode(found))

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
