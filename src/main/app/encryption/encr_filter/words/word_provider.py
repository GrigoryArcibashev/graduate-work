from src.main.app.encryption.encr_filter.words.word_loader import WordLoader


class WordProvider:
    def __init__(self, word_loader: WordLoader):
        self._words = set(word_loader.load())

    def check_word(self, word) -> bool:
        return word in self._words
