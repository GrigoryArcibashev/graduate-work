import unittest

from src.main.app.model.extractors import Word
from src.main.app.model.extractors import WordExtractor


class TestWordExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self._extractor = WordExtractor()

    def test__is_new_word(self):
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
        expected = expected_low = Word(string)

        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, *actual_low)

        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_one_letter2(self):
        string = tuple(b'A')

        expected = Word(string)
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

        expected_low = Word(tuple(b'a'))
        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, *actual_low)

    def test_camel_case1(self):
        string = tuple(b'first')
        expected = expected_low = Word(string)

        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, *actual_low)

        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_camel_case2(self):
        string = tuple(b'firstSecond')

        expected_low = list(map(self._map_str_to_word, ['first', 'second']))
        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, actual_low)

        expected = list(map(self._map_str_to_word, ['first', 'Second']))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, actual)

    def test_pascal_case1(self):
        string = tuple(b'First')

        expected_low = self._map_str_to_word('first')
        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, *actual_low)

        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        expected = self._map_str_to_word('First')
        self.assertEqual(expected, *actual)

    def test_pascal_case2(self):
        string = tuple(b'FirstSecond')

        expected_low = list(map(self._map_str_to_word, ['first', 'second']))
        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, actual_low)

        expected = list(map(self._map_str_to_word, ['First', 'Second']))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, actual)

    def test_one_upper_word(self):
        string = tuple(b'FIRST')
        expected = self._map_str_to_word('FIRST')
        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, *actual)

    def test_small_and_upper_words(self):
        string = tuple(b'firstSECOND')

        expected_low = list(map(self._map_str_to_word, ['first', 'second']))
        actual_low = list(self._extractor.get_word_iter(string, to_lower=True))
        self.assertEqual(expected_low, actual_low)

        expected = list(map(self._map_str_to_word, ['first', 'SECOND']))
        actual = list(self._extractor.get_word_iter(string, to_lower=False))
        self.assertEqual(expected, actual)

    @staticmethod
    def _map_str_to_word(string: str) -> Word:
        return Word(list(map(ord, string)))


if __name__ == '__main__':
    unittest.main()
