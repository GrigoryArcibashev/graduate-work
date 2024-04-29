from typing import Optional

from src.main.app.extractors.token_extractor import TokenExtractor
from src.main.app.extractors.word import Word
from src.main.app.extractors.word_extractor import WordExtractor
from src.main.app.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.obfuscation.name_processor import NameInfo, NameProcessor
from src.main.app.obfuscation.searchers.searchers import ClassSearcher, FunctionSearcher, VariableSearcher
from src.main.app.util.file_reader import read_file
from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.words_service.word_loader import SimpleWordLoader


class ObfuscationResult:
    def __init__(self, prop_of_obf_names: Optional[float] = None, max_allow_prop: Optional[float] = None):
        self._prop_of_obf_names = round(prop_of_obf_names, 2) if prop_of_obf_names else prop_of_obf_names
        self._max_allow_prop = round(max_allow_prop, 2) if max_allow_prop else max_allow_prop

    @property
    def is_obf(self) -> bool:
        if self._prop_of_obf_names and self._max_allow_prop:
            return self._prop_of_obf_names > self._max_allow_prop
        return False

    @property
    def proportion_of_obf_names(self) -> float:
        return self._prop_of_obf_names

    @property
    def max_allowable_proportion(self) -> float:
        return self._max_allow_prop

    def to_str(self) -> str:
        if self.is_obf:
            return f'OBF ({self.proportion_of_obf_names} > {self.max_allowable_proportion})'
        return f'NO OBF ({self.proportion_of_obf_names} <= {self.max_allowable_proportion})'

    def __str__(self):
        return self.to_str()


class ObfuscationDeterminator:
    def __init__(
            self,
            name_processor: NameProcessor,
            searcher_by_levenshtein_metric: SearcherByLevenshteinMetric
    ):
        self._searcher_by_levenshtein_metric = searcher_by_levenshtein_metric
        self._name_processor = name_processor
        self._obf_text_border = 0.5
        self._obf_name_border = 0.4
        self._words: dict[Word, bool] = dict()

    def _clear_words(self) -> None:
        self._words.clear()

    def determinate(self, text: bytes) -> ObfuscationResult:
        self._clear_words()
        count = obf_count = 0
        for name_info in self._name_processor.get_next_name_info(text):
            count += 1
            if self.is_obfuscated_name(name_info):
                obf_count += 1
        return ObfuscationResult(obf_count / count if count else 0, self._obf_text_border)

    def is_obfuscated_name(self, name_info: NameInfo) -> bool:
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
            result = self._searcher_by_levenshtein_metric.search(word)
            obf_word_count += not bool(result)
            self._words[word] = not bool(result)
        return not word_count or obf_word_count / word_count > self._obf_name_border


def main():
    tn_ext = TokenExtractor()
    var_searcher = VariableSearcher(tn_ext)
    func_searcher = FunctionSearcher(tn_ext)
    class_searcher = ClassSearcher(tn_ext)
    name_processor = NameProcessor([var_searcher, func_searcher, class_searcher], WordExtractor())

    word_dict_service = WordDictService(SimpleWordLoader('../words_service/words_by_len.bin'))
    obf_det = ObfuscationDeterminator(name_processor, SearcherByLevenshteinMetric(word_dict_service))

    result = obf_det.determinate(read_file('../../source/obf/obf_js.txt'))
    print(result)


if __name__ == '__main__':
    main()
