import unittest
from itertools import combinations

from src.main.app.extractors.token import Token, TokenType


class TestToken(unittest.TestCase):
    def test_equal_when_same_vals_and_types(self):
        val = [1, 2, 3]
        for type_ in TokenType:
            t1 = Token(val, type_)
            t2 = Token(val, type_)
            self.assertEqual(t1, t2)

    def test_not_equal_when_different_vals_and_same_types(self):
        val1 = [1, 2, 3]
        val2 = [1, 2]
        for type_ in TokenType:
            t1 = Token(val1, type_)
            t2 = Token(val2, type_)
            self.assertNotEqual(t1, t2)

    def test_not_equal_when_different_types_and_same_vals(self):
        val = [1, 2, 3]
        types = [t for t in TokenType]
        for type1, type2 in list(combinations(types, 2)):
            t1 = Token(val, type1)
            t2 = Token(val, type2)
            self.assertNotEqual(t1, t2)

    def test_hash(self):
        t1 = Token([1, 2], TokenType.DIGITS)
        t2 = Token([1, 2, 3], TokenType.DIGITS)
        t3 = Token([1, 2], TokenType.LETTERS)
        t4 = Token([1, 2, 3, 4], TokenType.OTHER)
        t5 = Token([1, 2, 3, 4], TokenType.OTHER)
        list_ = [t1, t2, t3, t4, t5]
        set_ = set(list_)

        self.assertEqual(len(set_), 4)
        for token in list_:
            self.assertIn(token, set_)

    def test_len(self):
        list_ = [
            Token([], TokenType.OTHER),
            Token([1, ], TokenType.OTHER),
            Token([1, 2, 3, 4, 5], TokenType.OTHER),
        ]
        for token in list_:
            self.assertEqual(len(token.value), len(token))


if __name__ == '__main__':
    unittest.main()
