import unittest

from src.main.app.words_service.word_provider import WordProvider
from src.test.test_words_service.util import *
from src.main.app.words_service.word_loader import SimpleWordLoader


class TestWordProvider(unittest.TestCase):
    def setUp(self) -> None:
        self._path = 'words_service.txt'
        self._loader = SimpleWordLoader(self._path)

    def test_true(self):
        words = ['this', 'is', 'test']
        write_test_words(words, self._path)
        provider = WordProvider(self._loader)
        for word in words:
            act = provider.check_word(map_str_to_numbers(word))
            self.assertEqual(act, True)

    def test_false(self):
        words = ['this', 'is', 'test']
        write_test_words(words, self._path)
        provider = WordProvider(self._loader)
        act = provider.check_word(map_str_to_numbers('word'))
        self.assertEqual(act, False)


if __name__ == '__main__':
    unittest.main()
