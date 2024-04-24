import pathlib
import unittest

from src.main.app.words_service.word_loader import AbstractWordLoader, SimpleWordLoader
from src.test.test_words_service.util import WordMakerForTests, write_word_dict


class TestWordLoader(unittest.TestCase):
    def setUp(self) -> None:
        self._path = 'path'

    def test_when_path_to_words_is_set_during_init(self):
        loader = AbstractWordLoader(self._path)
        self.assertEqual(loader.path, self._path)

    def test_when_path_to_words_is_set_after_init(self):
        loader = AbstractWordLoader()
        self.assertEqual(loader.path, None)
        loader.path = self._path
        self.assertEqual(loader.path, self._path)

    def test_load(self):
        with self.assertRaises(NotImplementedError):
            AbstractWordLoader(self._path).load()


class TestSimpleWordLoader(unittest.TestCase):
    def setUp(self) -> None:
        _paths = [
            pathlib.Path('source/words_by_len.bin').absolute(),
            pathlib.Path('../source/words_by_len.bin').absolute(),
        ]
        self._path = str(list(filter(lambda p: p.exists(), _paths))[0])

    def test_load(self):
        writer = WordMakerForTests()
        words = 'these are the words for the test'.split()
        word_dict = writer.make(words)
        write_word_dict(word_dict, self._path)

        loaded = SimpleWordLoader(self._path).load()
        self.assertEqual(loaded, word_dict)


if __name__ == '__main__':
    unittest.main()
