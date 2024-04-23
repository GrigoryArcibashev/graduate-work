import unittest

from src.main.app.extractors.word import Word
from src.main.app.extractors.word_extractor import WordExtractor


class TestWordExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self._extractor = WordExtractor()

    def test__is_new_lexeme(self):
        strings_false = [
            (None, b'a'),
            (None, b'A'),
            (b'a', b'a'),
            (b'A', b'a'),
            (b'A', b'A')
        ]
        strings_true = [(b'a', b'A')]

        to_ord = lambda _str: list(map(lambda sym: ord(sym) if sym else sym, _str))
        for string in strings_false:
            actual = self._extractor.is_new_word(*to_ord(string))
            self.assertEqual(actual, False)
        for string in strings_true:
            actual = self._extractor.is_new_word(*to_ord(string))
            self.assertEqual(actual, True)

    def test_one_letter1(self):
        string = tuple(b'a')
        expected = Word(string)
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_one_letter2(self):
        string = tuple(b'A')
        expected = Word(string)
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_camel_case1(self):
        string = tuple(b'first')
        expected = Word(string)
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_camel_case2(self):
        string = tuple(b'firstSecond')
        expected = list(map(self._map_str_to_word, ['first', 'Second']))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, actual)

    def test_pascal_case1(self):
        string = tuple(b'First')
        expected = self._map_str_to_word('First')
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_pascal_case2(self):
        string = tuple(b'FirstSecond')
        expected = list(map(self._map_str_to_word, ['First', 'Second']))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, actual)

    def test_one_upper_word(self):
        string = tuple(b'FIRST')
        expected = self._map_str_to_word('FIRST')
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_small_and_upper_words(self):
        string = tuple(b'firstSECOND')
        expected = list(map(self._map_str_to_word, ['first', 'SECOND']))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, actual)

    @staticmethod
    def _map_str_to_word(string: str) -> Word:
        return Word(list(map(ord, string)))


if __name__ == '__main__':
    unittest.main()
