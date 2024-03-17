import unittest

from src.main.app.encryption.token_extractor import TokenExtractor, Token, TokenType


class Test(unittest.TestCase):
    def test_simplest_letters(self):
        string = b'first'
        expected = self._make_tokens_by_mapping_from_str_values([Token('first', TokenType.LETTERS)])
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_simplest_digits(self):
        string = b'1234'
        expected = self._make_tokens_by_mapping_from_str_values([Token('1234', TokenType.DIGITS)])
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_simplest_other(self):
        string = b'*!$'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('*', TokenType.OTHER),
                Token('!', TokenType.OTHER),
                Token('$', TokenType.OTHER)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_camel_case(self):
        string = b'firstSecondThird'
        expected = self._make_tokens_by_mapping_from_str_values([Token('firstSecondThird', TokenType.LETTERS)])
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_snake_case(self):
        string = b'first_second_Third'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('first', TokenType.LETTERS),
                Token('_', TokenType.OTHER),
                Token('second', TokenType.LETTERS),
                Token('_', TokenType.OTHER),
                Token('Third', TokenType.LETTERS)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_string_with_spaces1(self):
        string = b'first second  3 '
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('first', TokenType.LETTERS),
                Token(' ', TokenType.OTHER),
                Token('second', TokenType.LETTERS),
                Token(' ', TokenType.OTHER),
                Token(' ', TokenType.OTHER),
                Token('3', TokenType.DIGITS),
                Token(' ', TokenType.OTHER)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_string_with_spaces2(self):
        string = b'first\nsecond'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('first', TokenType.LETTERS),
                Token('\n', TokenType.OTHER),
                Token('second', TokenType.LETTERS)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_string_with_spaces3(self):
        string = b'\r\nfirst second \n'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('\r', TokenType.OTHER),
                Token('\n', TokenType.OTHER),
                Token('first', TokenType.LETTERS),
                Token(' ', TokenType.OTHER),
                Token('second', TokenType.LETTERS),
                Token(' ', TokenType.OTHER),
                Token('\n', TokenType.OTHER)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_simple1(self):
        string = b'four+5=9'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('four', TokenType.LETTERS),
                Token('+', TokenType.OTHER),
                Token('5', TokenType.DIGITS),
                Token('=', TokenType.OTHER),
                Token('9', TokenType.DIGITS)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_simple2(self):
        string = b'TwentyOne-6 == 15!'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('TwentyOne', TokenType.LETTERS),
                Token('-', TokenType.OTHER),
                Token('6', TokenType.DIGITS),
                Token(' ', TokenType.OTHER),
                Token('=', TokenType.OTHER),
                Token('=', TokenType.OTHER),
                Token(' ', TokenType.OTHER),
                Token('15', TokenType.DIGITS),
                Token('!', TokenType.OTHER)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def test_php_variable_assignment(self):
        string = b'$num = 10;'
        expected = self._make_tokens_by_mapping_from_str_values(
            [
                Token('$', TokenType.OTHER),
                Token('num', TokenType.LETTERS),
                Token(' ', TokenType.OTHER),
                Token('=', TokenType.OTHER),
                Token(' ', TokenType.OTHER),
                Token('10', TokenType.DIGITS),
                Token(';', TokenType.OTHER)
            ]
        )
        actual = TokenExtractor().extract_tokens_from_string(string)
        self.assertEqual(actual, expected)

    def _make_tokens_by_mapping_from_str_values(self, tokens: list[Token[str, TokenType]]) \
            -> list[Token[list[int], TokenType]]:
        return list(map(self._map_str_val_to_numbers, tokens))

    @staticmethod
    def _map_str_val_to_numbers(token: Token[str, TokenType]) -> Token[list[int], TokenType]:
        new_val = list(map(ord, token.value))
        return Token(new_val, token.type)

    def _print(self, tokens: list[Token]) -> None:
        print()
        for token in tokens:
            print(f'{repr(self._convert_numbers_of_bytes_to_str(token.value))} -> {token.type}')

    @staticmethod
    def _convert_numbers_of_bytes_to_str(numbers: list[int]) -> str:
        return ''.join(tuple(map(chr, numbers)))


if __name__ == '__main__':
    unittest.main()
