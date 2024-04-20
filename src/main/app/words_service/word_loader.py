from abc import abstractmethod

from src.main.app.file_reader import read_file_by_pickle


class WordLoader:
    def __init__(self, path: str = None):
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, new: str) -> None:
        self._path = new

    @abstractmethod
    def load(self) -> dict[int, set[tuple[int]]]:
        pass


class SimpleWordLoader(WordLoader):
    def load(self) -> dict[int, set[tuple[int]]]:
        return read_file_by_pickle(self.path)
