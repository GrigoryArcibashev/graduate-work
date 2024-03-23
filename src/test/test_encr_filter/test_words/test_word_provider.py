import unittest

from src.main.app.encryption.encr_filter.words.word_provider import WordProvider
from src.test.test_encr_filter.test_words.util import *
from src.main.app.encryption.encr_filter.words.word_loader import SimpleWordLoader


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self._path = 'words.txt'
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