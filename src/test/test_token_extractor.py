import unittest

from src.main.app.encryption.token_extractor import TokenExtractor


class Test(unittest.TestCase):
    def test_simple(self):
        string = b'firstSecond_third#four_FiveSix__seven=eight123_45%^&nine'
        print()
        for token in TokenExtractor().extract_tokens_from_string(string):
            val_as_str = ''.join(tuple(map(chr, token.value)))
            print(f'{val_as_str} -> {token.type}')


if __name__ == '__main__':
    unittest.main()
