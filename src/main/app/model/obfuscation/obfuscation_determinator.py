from typing import Optional

from src.main.app.model.extractors.word import Word
from src.main.app.model.obfuscation.levenshtein_metric import SearcherByLevenshteinMetric
from src.main.app.model.obfuscation.name_processor import NameInfo, NameProcessor
from src.main.app.model.settings.obfuscation_determinator_settings import ObfuscationDetSettings


class ObfuscationResult:
    def __init__(
            self,
            is_obf: bool,
            prop_of_obf_names: Optional[float] = None,
            max_allow_prop: Optional[float] = None
    ):
        self._is_obf = is_obf
        self._prop_of_obf_names = round(prop_of_obf_names, 2) if prop_of_obf_names else prop_of_obf_names
        self._max_allow_prop = round(max_allow_prop, 2) if max_allow_prop else max_allow_prop

    @property
    def is_obf(self) -> bool:
        return self._is_obf

    @property
    def proportion_of_obf_names(self) -> Optional[float]:
        return self._prop_of_obf_names

    @property
    def max_allowable_proportion(self) -> Optional[float]:
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
            searcher_by_levenshtein_metric: SearcherByLevenshteinMetric,
            settings: ObfuscationDetSettings
    ):
        self._searcher_by_levenshtein_metric = searcher_by_levenshtein_metric
        self._name_processor = name_processor
        self._obf_text_border = settings.obf_text_border
        self._obf_name_border = settings.obf_name_border
        self._max_non_obf_count_digits = settings.max_non_obf_count_digits
        self._is_obf_word: dict[Word, bool] = dict()

    def _clear_words(self) -> None:
        self._is_obf_word.clear()

    def determinate(self, text: bytes) -> ObfuscationResult:
        obf_count, count = self._determine_number_of_unique_obf_names(text)
        prop_of_obf_names = obf_count / count if count else 0
        return ObfuscationResult(prop_of_obf_names > self._obf_text_border, prop_of_obf_names, self._obf_text_border)

    def _determine_number_of_unique_obf_names(self, text: bytes) -> (int, int):
        self._clear_words()
        count = obf_count = 0
        for name_info in self._name_processor.get_next_name_info(text):
            count += 1
            if self.is_obfuscated_name(name_info):
                obf_count += 1
        return obf_count, count

    def is_obfuscated_name(self, name_info: NameInfo) -> bool:
        if name_info.digit_len > self._max_non_obf_count_digits:
            return True
        word_count = obf_word_count = 0
        for word in filter(lambda w: len(w) > 1, name_info.words):
            if word not in self._is_obf_word:
                searched_word, _ = self._searcher_by_levenshtein_metric.search(word)
                self._is_obf_word[word] = not bool(searched_word)
            obf_word_count += int(self._is_obf_word[word])
            word_count += 1
        return not word_count or obf_word_count / word_count > self._obf_name_border
