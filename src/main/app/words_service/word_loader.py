from abc import abstractmethod

from src.main.app.extractors.word import Word
from src.main.app.file_reader import read_file_by_pickle


class AbstractWordLoader:
    """Загружает словарь слов в память"""

    def __init__(self, path: str = None):
        self._path = path

    @property
    def path(self) -> str:
        """
        :return: путь до словаря слов
        """
        return self._path

    @path.setter
    def path(self, new: str) -> None:
        """
        Устанавливает путь до словаря слов

        :param new: новый путь до словаря слов

        :return: None
        """
        self._path = new

    @abstractmethod
    def load(self) -> dict[int, set[Word]]:
        """
        Загружает словарь слов (по пути path) в память в виде dict[длина слова] = {слова}

        :return: загруженный словарь
        """
        raise NotImplementedError()


class SimpleWordLoader(AbstractWordLoader):
    def load(self) -> dict[int, set[Word]]:
        return read_file_by_pickle(self.path)
