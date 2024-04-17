from src.main.app.encryption.encr_filter.words.word_loader import SimpleWordLoader
from src.main.app.encryption.encr_filter.words.word_provider import WordProvider
from src.main.app.encryption.extractors.word_extractor import Word
from src.main.app.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.obfuscation.name_processor import NameInfo, NameProcessor


class ObfuscationChecker:
    def __init__(self, searcher_by_levenshtein_metric: SearcherByLevenshteinMetric):
        self._searcher_by_levenshtein_metric = searcher_by_levenshtein_metric

    def is_obfuscated(self, name_info: NameInfo) -> bool:
        obf_count = 0
        for word in name_info.words:
            k = round(0.4 * len(word))
            result = self._searcher_by_levenshtein_metric.search(word, k)
            print(f'{word}')
            print('OBF' if result is None else f'{result[1]}: {result[0]}', end='\n\n')
            if result is None:
                obf_count += 1
        return obf_count / len(name_info.words) >= 0.5


class ObfuscationDeterminator:
    def __init__(self, name_processor: NameProcessor, obfuscation_checker: ObfuscationChecker):
        self._name_processor = name_processor
        self._obfuscation_checker = obfuscation_checker

    def determinate(self, text):
        count = obf_count = 0
        for name_info in self._name_processor.get_next_name_info(text):
            count += 1
            if self._obfuscation_checker.is_obfuscated(name_info):
                obf_count += 1
        return obf_count / count >= 0.5


def main():
    checker = ObfuscationChecker(
        SearcherByLevenshteinMetric(
            WordProvider(
                SimpleWordLoader('../encryption/encr_filter/words/words_by_len.bin')
            )
        )
    )
    str_words = ['aabcxec', 'uuebfuea', 'iioavyanev']
    words = []
    for word in str_words:
        words.append(Word(list(map(ord, list(word)))))
    print(checker.is_obfuscated(NameInfo(words, 0, 0)))


if __name__ == '__main__':
    main()
