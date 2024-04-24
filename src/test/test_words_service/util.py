import os.path
import pathlib
import pickle

from src.main.app.extractors.word import Word


def write_word_dict(word_dict: dict[int, set[Word]], path_to_write: str):
    with open(path_to_write, 'wb') as f:
        pickle.dump(word_dict, f)


class WordMakerForTests:
    """Создает словарь слов ( dict[len] = {Words} )"""

    def make(self, words: list[str]) -> dict[int, set[Word]]:
        return self._make_word_dict(self._make_words(words))

    @staticmethod
    def _map_to_number(word: str) -> tuple[int]:
        return tuple(map(ord, word))

    def _make_words(self, words: list[str]) -> list[Word]:
        return list(map(lambda word: Word(self._map_to_number(word)), words))

    @staticmethod
    def _make_word_dict(words: list[Word]) -> dict[int, set[Word]]:
        result = dict()
        for word in words:
            length = len(word)
            if length not in result:
                result[length] = set()
            result[length].add(word)
        return result


# if __name__ == '__main__':
#     path = pathlib.Path('test/source/words_by_len.bin').absolute()
#     print(os.path.exists(path))
