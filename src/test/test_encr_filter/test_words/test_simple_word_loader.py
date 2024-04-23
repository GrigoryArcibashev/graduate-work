import unittest

from src.main.app.words_service.word_loader import SimpleWordLoader
from src.test.test_encr_filter.test_words.util import *


class TestSimpleWordLoader(unittest.TestCase):
    def setUp(self) -> None:
        self._path = 'words_service.txt'

    def test_when_path_to_words_is_set_during_init(self):
        loader = SimpleWordLoader(self._path)
        self.assertEqual(loader.path, self._path)

    def test_when_path_to_words_is_set_after_init(self):
        loader = SimpleWordLoader()
        self.assertEqual(loader.path, None)
        loader.path = self._path
        self.assertEqual(loader.path, self._path)

    def test_load(self):
        words = ['this', 'is', 'simple', 'test']
        write_test_words(words, self._path)
        loaded = SimpleWordLoader(self._path).load()
        self.assertEqual(loaded, list(map(map_str_to_numbers, words)))


if __name__ == '__main__':
    unittest.main()
