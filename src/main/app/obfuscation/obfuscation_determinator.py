from src.main.app.words_service.word_loader import SimpleWordLoader
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.extractors.token_extractor import TokenExtractor
from src.main.app.extractors.word import Word
from src.main.app.extractors.word_extractor import WordExtractor
from src.main.app.file_reader import read_file
from src.main.app.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.obfuscation.name_processor import NameInfo, NameProcessor
from src.main.app.obfuscation.searchers.searchers import VariableSearcher, FunctionSearcher, ClassSearcher


class ObfuscationDeterminator:
    def __init__(
            self,
            name_processor: NameProcessor,
            searcher_by_levenshtein_metric: SearcherByLevenshteinMetric
    ):
        self._searcher_by_levenshtein_metric = searcher_by_levenshtein_metric
        self._name_processor = name_processor
        self._obf_text_border = 0.35
        self._obf_name_border = 0.35
        self._words: dict[Word, bool] = dict()

    def _clear_words(self) -> None:
        self._words.clear()

    def determinate(self, text: bytes) -> bool:
        self._clear_words()
        count = obf_count = 0
        for name_info in self._name_processor.get_next_name_info(text):
            count += 1
            if self.is_obfuscated(name_info):
                obf_count += 1
        print_res = round(obf_count / max(1, count), 2)
        print(f'\nobf_count ({obf_count}) / count ({count}) = {print_res} ', end='')
        print(f'[{">=" if print_res >= self._obf_text_border else "<"}{self._obf_text_border}]')
        return count and obf_count / count >= self._obf_text_border

    def is_obfuscated(self, name_info: NameInfo) -> bool:
        if name_info.digit_len > 4:
            return True
        if name_info.letters_len < 3 and name_info.digit_len < 2:
            return False
        word_count = obf_word_count = 0
        for word in name_info.words:
            if len(word) < 2:
                continue
            word_count += 1
            if word in self._words:
                obf_word_count += int(self._words[word])
                continue
            k = self._calc_max_levenshtein_distance(word)
            result = self._searcher_by_levenshtein_metric.search(word, k)
            print(f'{word}')
            print('OBF' if result is None else f'NON OBF\n{result[1]} : {result[0]}', end='\n\n')
            obf_word_count += not bool(result)
            self._words[word] = not bool(result)
        return not word_count or obf_word_count / word_count >= self._obf_name_border

    @staticmethod
    def _calc_max_levenshtein_distance(word: Word) -> int:
        if len(word) < 3:
            return 0
        if len(word) < 5:
            return 1
        if len(word) < 7:
            return 2
        if len(word) < 10:
            return 3
        return round(0.35 * len(word))


def main():
    var_searcher = VariableSearcher(TokenExtractor())
    func_searcher = FunctionSearcher(TokenExtractor())
    class_searcher = ClassSearcher(TokenExtractor())
    processor = NameProcessor([var_searcher, func_searcher, class_searcher], WordExtractor())
    checker = ObfuscationDeterminator(
        name_processor=processor,
        searcher_by_levenshtein_metric=SearcherByLevenshteinMetric(
            WordDictService(
                SimpleWordLoader('../words_service/words_by_len.bin')
            )
        )
    )
    text = read_file('../../source/x.txt')
    # text = input().encode()
    is_obf_text = checker.determinate(text)
    print(f"VERDICT: {'OBF' if is_obf_text else 'NO OBF'}")


if __name__ == '__main__':
    main()
