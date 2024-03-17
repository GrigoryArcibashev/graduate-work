import unittest

from src.main.app.encryption.token_extractor import TokenExtractor


class Test(unittest.TestCase):
    def test_simple(self):
        string = b'firstSecond_third#four_FiveSix__seven=eight123_45%^&nine'
        self._print(TokenExtractor().extract_tokens_from_string(string))

    def test_string_with_space(self):
        string = b'first second  third\nfour\r\nfive'
        self._print(TokenExtractor().extract_tokens_from_string(string))

    @staticmethod
    def _print(tokens):
        print()
        for token in tokens:
            val_as_str = ''.join(tuple(map(chr, token.value)))
            print(f'{repr(val_as_str)} -> {token.type}')


if __name__ == '__main__':
    unittest.main()
