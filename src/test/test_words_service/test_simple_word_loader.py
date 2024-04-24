import os
import pathlib
import unittest

from src.main.app.extractors.word import Word
from src.main.app.words_service.word_loader import SimpleWordLoader
from src.test.test_words_service.util import WordMakerForTests, write_word_dict


class TestSimpleWordLoader(unittest.TestCase):
    def test_when_path_to_words_is_set_during_init(self):
        loader = SimpleWordLoader(self._path)
        self.assertEqual(loader.path, self._path)

    def test_when_path_to_words_is_set_after_init(self):
        loader = SimpleWordLoader()
        self.assertEqual(loader.path, None)
        loader.path = self._path
        self.assertEqual(loader.path, self._path)

    def test_load(self):
        writer = WordMakerForTests()
        words = 'these are the words for the test'.split()
        path = pathlib.Path('test/source/words_by_len.bin').absolute()
        word_dict = writer.make(words)
        write_word_dict(word_dict, str(path))

        loaded = SimpleWordLoader(str(path)).load()
        self.assertEqual(loaded, word_dict)


if __name__ == '__main__':
    unittest.main()
