import unittest

from src.main.app.words_service.word_provider import WordDictService
from src.test.test_words_service.util import *
from src.main.app.words_service.word_loader import SimpleWordLoader


class TestWordProvider(unittest.TestCase):
    def setUp(self) -> None:
        _paths = [
            pathlib.Path('source/words_by_len.bin').absolute(),
            pathlib.Path('../source/words_by_len.bin').absolute(),
        ]
        self._path = str(list(filter(lambda p: p.exists(), _paths))[0])
        self._loader = SimpleWordLoader(self._path)


if __name__ == '__main__':
    unittest.main()
