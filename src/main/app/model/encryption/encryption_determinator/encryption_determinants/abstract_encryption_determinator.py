from abc import abstractmethod
from typing import Union

from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode


class AbstractEncryptionDeterminator:
    """
    Абстрактный определитель шифра
    """

    def __init__(self):
        self._mode = None

    @property
    def mode(self) -> OperatingMode:
        """
        Возвращает режим работы определителя

        :return: режим работы определителя
        """
        return self._mode

    @mode.setter
    def mode(self, mode: OperatingMode) -> None:
        """
        Устанавливает режим работы определителя

        :param mode: режим работы определителя
        :return: None
        """
        self._mode = mode

    @abstractmethod
    def determinate(self, data: Union[list[int], bytes]):
        """
        Определяет наличие шифра в тексте

        :param data: текст
        :return: см. реализацию
        """
        raise NotImplementedError()
