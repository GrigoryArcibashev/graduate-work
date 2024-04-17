from src.main.app.encryption.encr_filter.words.word_loader import SimpleWordLoader
from src.main.app.encryption.encr_filter.words.word_provider import WordProvider
from src.main.app.encryption.extractors.word_extractor import Word
from src.main.app.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.obfuscation.name_processor import NameInfo, NameProcessor


class ObfuscationChecker:
    def __init__(self, searcher_by_levenshtein_metric: SearcherByLevenshteinMetric):
        self._searcher_by_levenshtein_metric = searcher_by_levenshtein_metric

    # def check(self, name_info: NameInfo) -> bool:
    #     """
    #     :return: True (obf) / False (no obf)
    #     """
    #     for word in name_info.words:
    #         k = round(0.4 * len(word))
    #         result = self._searcher_by_levenshtein_metric.search(word, k)
    #         print(result)
    #     return True
    def check(self, words):
        for word in words:
            k = round(0.4 * len(word))
            result = self._searcher_by_levenshtein_metric.search(word, k, first_appropriate=False)
            print(f'{word}')
            print('None' if result is None else f'{result[1]}: {result[0]}', end='\n\n')


class ObfuscationDeterminator:
    def __init__(self, name_processor: NameProcessor, obfuscation_checker: ObfuscationChecker):
        self._name_processor = name_processor
        self._obfuscation_checker = obfuscation_checker

    def determinate(self, text):
        count = obf_count = 0
        for name_info in self._name_processor.get_next_name_info(text):
            count += 1
            if self._obfuscation_checker.check(name_info):
                obf_count += 1
        # TODO переделать
        return round(100 * obf_count / count, 2)


def main():
    checker = ObfuscationChecker(
        SearcherByLevenshteinMetric(
            WordProvider(
                SimpleWordLoader('../encryption/encr_filter/words/words_by_len.bin')
            )
        )
    )
    str_words = ['impor', 'excet', 'acknlegment']
    words = []
    for word in str_words:
        words.append(Word(list(map(ord, list(word)))))
    checker.check(words)


if __name__ == '__main__':
    main()
