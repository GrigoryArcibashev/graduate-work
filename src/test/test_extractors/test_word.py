import unittest

from src.main.app.model.extractors import Word


class TestToken(unittest.TestCase):
    def test_equal_same_values(self):
        val = [1, 2, 3]
        self.assertEqual(True, Word(val) == Word(val))

    def test_not_equal_different_objs(self):
        with self.assertRaises(TypeError):
            _raise = Word([]) == list()

    def test_not_equal_different_values(self):
        val1 = [1, 2, 3]
        val2 = [1, 2, 3, 4]
        self.assertEqual(False, Word(val1) == Word(val2))

    def test_hash(self):
        w1 = Word([1, 2])
        w2 = Word([1, 2, 3])
        w3 = Word([1, 2, 3, 4])
        w4 = Word([1, 2, 3, 4])
        list_ = [w1, w2, w3, w4]
        set_ = set(list_)

        self.assertEqual(len(set_), 3)
        for word in list_:
            self.assertIn(word, set_)

    def test_len(self):
        list_ = [
            Word([]),
            Word([1, ]),
            Word([1, 2, 3]),
        ]
        for word in list_:
            self.assertEqual(len(word.value), len(word))

    def test_str(self):
        str(Word([100, 101, 102]))


if __name__ == '__main__':
    unittest.main()
