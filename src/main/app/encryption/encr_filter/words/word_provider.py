from src.main.app.encryption.encr_filter.words.word_loader import WordLoader
from src.main.app.encryption.extractors.word_extractor import Word


class WordProvider:
    def __init__(self, word_loader: WordLoader):
        self._words_by_len = word_loader.load()

    def check_word(self, word: Word) -> bool:
        result = len(word) in self._words_by_len and word.value in self._words_by_len[len(word)]
        return result
