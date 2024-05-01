from src.main.app.extractors.word import Word
from src.main.app.words_service.word_dict_service import WordDictService


class CalculatorLevenshteinMetric:
    def __init__(self):
        self._insert_cost: int = 1
        self._delete_cost: int = 1
        self._replace_cost: int = 1
        if not self._is_costs_valid(self._insert_cost, self._delete_cost, self._replace_cost):
            raise ValueError("The costs must be non-negative")

    def calculate(self, word1: Word, word2: Word) -> int:
        """
        Алгоритм Вагнера-Фишера.

        Временная сложность O(nm).

        Память O(min(n, m)).
        :param word1: слово (Word) длины n
        :param word2: слово (Word) длины m
        :return: (int) расстояние Левенштейна
        """
        word1, word2 = self._get_words_in_ascending_order_of_length(word1, word2)
        len_word1, len_word2 = len(word1), len(word2)
        current_row = range(len_word1 + 1)
        for y in range(1, len_word2 + 1):
            prev_row, current_row = current_row, [y] + [0] * len_word1
            for x in range(1, len_word1 + 1):
                insert = prev_row[x] + self._insert_cost
                delete = current_row[x - 1] + self._delete_cost
                replace = prev_row[x - 1]
                if word1.value[x - 1] != word2.value[y - 1]:
                    replace += self._replace_cost
                current_row[x] = min(insert, delete, replace)
        return current_row[len_word1]

    @staticmethod
    def _is_costs_valid(insert_cost: int, delete_cost: int, replace_cost: int) -> bool:
        return (
                insert_cost and insert_cost >= 0
                or delete_cost and delete_cost >= 0
                or replace_cost and replace_cost >= 0
        )

    @staticmethod
    def _get_words_in_ascending_order_of_length(word1: Word, word2: Word) -> (Word, Word):
        if len(word1) > len(word2):
            word1, word2 = word2, word1
        return word1, word2


class SearcherByLevenshteinMetric:
    def __init__(self, word_dict_service: WordDictService):
        self._word_dict_service = word_dict_service
        self._metric_calculator = CalculatorLevenshteinMetric()
        self._mult_for_max_lev_distance = 0.35

    def search(self, word: Word) -> (Word, int):
        if self._word_dict_service.check_word(word):
            return word, 0
        max_distance = self._calc_max_levenshtein_distance(word)
        order = self.get_len_order(len(word), max_distance)
        for length in order:
            dict_words = self._word_dict_service.get_words_with_len(length)
            for dict_word in dict_words:
                metric = self._metric_calculator.calculate(word, dict_word)
                if metric <= max_distance:
                    return dict_word, metric
        return None, None

    def get_len_order(self, word_len: int, k: int) -> list[int]:
        if (
                word_len - k > self._word_dict_service.get_max_len()
                or word_len + k < self._word_dict_service.get_min_len()
        ):
            return list()
        left = max(self._word_dict_service.get_min_len(), word_len - k)
        right = min(self._word_dict_service.get_max_len(), word_len + k)
        return sorted(range(left, right + 1), key=lambda x: abs(word_len - x))

    def _calc_max_levenshtein_distance(self, word: Word) -> int:
        return round(self._mult_for_max_lev_distance * len(word))


if __name__ == '__main__':
    lm = CalculatorLevenshteinMetric()
    w1 = Word([98, 100])
    w2 = Word([98, 99, 100])
    print(lm.calculate(w1, w2))
