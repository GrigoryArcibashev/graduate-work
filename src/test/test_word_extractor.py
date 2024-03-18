import unittest

from src.main.app.encryption.extractors.word_extractor import WordExtractor


class Test(unittest.TestCase):
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
            actual = self._extractor.is_new_lexeme(*to_ord(string))
            self.assertEqual(actual, False)
        for string in strings_true:
            actual = self._extractor.is_new_lexeme(*to_ord(string))
            self.assertEqual(actual, True)

    def test_one_letter1(self):
        string = b'a'
        expected = self._map_str_to_numbers('a')
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, *actual)

    def test_one_letter2(self):
        string = b'A'
        expected = self._map_str_to_numbers('A')
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, *actual)

    def test_camel_case1(self):
        string = b'first'
        expected = self._map_str_to_numbers('first')
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, *actual)

    def test_camel_case2(self):
        string = b'firstSecond'
        expected = list(map(self._map_str_to_numbers, ['first', 'Second']))
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, actual)

    def test_pascal_case1(self):
        string = b'First'
        expected = self._map_str_to_numbers('First')
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, *actual)

    def test_pascal_case2(self):
        string = b'FirstSecond'
        expected = list(map(self._map_str_to_numbers, ['First', 'Second']))
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, actual)

    def test_one_upper_word(self):
        string = b'FIRST'
        expected = self._map_str_to_numbers('FIRST')
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, *actual)

    def test_small_and_upper_words(self):
        string = b'firstSECOND'
        expected = list(map(self._map_str_to_numbers, ['first', 'SECOND']))
        actual = list(self._extractor.get_word_iter(string))
        self.assertEqual(expected, actual)

    @staticmethod
    def _map_str_to_numbers(string: str) -> list[int]:
        return list(map(ord, string))


if __name__ == '__main__':
    unittest.main()
