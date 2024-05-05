import pathlib
import unittest

from src.main.app.settings.word_loader_settings import WordLoaderSettings
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.words_service.word_loader import SimpleWordLoader
from src.test.test_words_service.util import WordMakerForTests, write_word_dict


class TestWordDictService(unittest.TestCase):
    def setUp(self) -> None:
        _paths = [
            pathlib.Path('source/words_by_len.bin').absolute(),
            pathlib.Path('../source/words_by_len.bin').absolute(),
        ]
        path = str(list(filter(lambda p: p.exists(), _paths))[0])

        self._words = 'one two three four five'.split()
        self._word_maker = WordMakerForTests()
        self._word_dict = self._word_maker.make_dict(self._words)
        write_word_dict(self._word_dict, path)

        self._service = WordDictService(SimpleWordLoader(WordLoaderSettings({'path_to_word_dict': path})))

    def test_get_min_len(self):
        self.assertEqual(min(self._word_dict), self._service.get_min_len())

    def test_get_max_len(self):
        self.assertEqual(max(self._word_dict), self._service.get_max_len())

    def test_get_words_with_len(self):
        for length in self._word_dict:
            self.assertEqual(self._service.get_words_with_len(length), self._word_dict.get(length))

    def test_get_words_with_len_when_is_None(self):
        max_len = max(self._word_dict)
        self.assertEqual(self._service.get_words_with_len(max_len + 1), None)

    def test_check_word_when_true(self):
        for word in self._word_maker.make_words(self._words):
            self.assertEqual(True, self._service.check_word(word))

    def test_check_word_when_false(self):
        for word in self._word_maker.make_words(['a' * 10, 'b' * 20]):
            self.assertEqual(False, self._service.check_word(word))


if __name__ == '__main__':
    unittest.main()
