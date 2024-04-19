from typing import Iterator

from src.main.app.encryption.extractors.token_extractor import TokenType, TokenExtractor
from src.main.app.encryption.extractors.word_extractor import WordExtractor, Word
from src.main.app.obfuscation.searchers.name import Name
from src.main.app.obfuscation.searchers.searchers import AbstractSearcher, VariableSearcher


class NameInfo:
    def __init__(self, words: list[Word], letters_len: int, digit_len: int):
        self._words = words
        self._letters_len = letters_len
        self._digit_len = digit_len

    @property
    def words(self) -> list[Word]:
        return self._words

    @property
    def letters_len(self) -> int:
        return self._letters_len

    @property
    def digit_len(self) -> int:
        return self._digit_len

    def __str__(self):
        return f'name_len: {self._letters_len}, digit_len: {self._digit_len}'


class NameProcessor:
    def __init__(self, searchers: list[AbstractSearcher], word_extractor: WordExtractor):
        self._searchers = searchers
        self._word_extractor = word_extractor

    def get_next_name_info(self, text) -> Iterator[NameInfo]:
        for searcher in self._searchers:
            for name in searcher.get_name_iter(text):
                yield self._make_name_info(name)

    def _make_name_info(self, name: Name) -> NameInfo:
        words = list()
        letters_len = digit_len = 0
        for token in name.value:
            if token.type == TokenType.LETTERS:
                letters_len += len(token)
                words.extend(list(self._word_extractor.get_word_iter(token.value)))
            else:
                digit_len += len(token)
        return NameInfo(words, letters_len, digit_len)


def main():
    variables = set()
    # text = b"let var1 = var2 = 12;"
    text = b"const var0 = 'string';\nlet var431 , var_var_2 = 12, 22;"
    var_searcher = VariableSearcher(TokenExtractor())
    processor = NameProcessor([var_searcher, ], WordExtractor())
    for var in var_searcher.get_name_iter(text):
        print('OLD' if var in variables else 'NEW', end=' VARIABLE\n')
        for name in var.value:
            print(f'\t{name}')
        print(processor._make_name_info(var))
        print()
        variables.add(var)


if __name__ == '__main__':
    main()
