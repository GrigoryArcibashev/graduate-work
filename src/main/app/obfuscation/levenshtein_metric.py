from src.main.app.encryption.extractors.word_extractor import Word


class CalculatorLevenshteinMetric:
    def calculate(
            self,
            word1: Word,
            word2: Word,
            insert_cost: int = 1,
            delete_cost: int = 1,
            replace_cost: int = 1
    ) -> int:
        """
        Алгоритм Вагнера-Фишера.

        Временная сложность O(nm).

        Память O(min(n, m)).
        :param word1: слово (Word) длины n
        :param word2: слово (Word) длины m
        :param insert_cost: (int) цена операции вставки
        :param delete_cost: (int) цена операции удаления
        :param replace_cost: (int) цена операции замены
        :return: (int) расстояние Левенштейна
        """
        if not self._is_costs_valid(insert_cost, delete_cost, replace_cost):
            raise ValueError("The costs must be non-negative")
        word1, word2 = self._get_words_in_ascending_order_of_length(word1, word2)
        len_word1, len_word2 = len(word1), len(word2)

        current_row = range(len_word1 + 1)
        for y in range(1, len_word2 + 1):
            prev_row, current_row = current_row, [y] + [0] * len_word1
            for x in range(1, len_word1 + 1):
                insert, delete, replace = prev_row[x] + 1, current_row[x - 1] + 1, prev_row[x - 1]
                if word1.value[x - 1] != word2.value[y - 1]:
                    replace += 1
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


if __name__ == '__main__':
    lm = CalculatorLevenshteinMetric()
    w1 = Word([98, 100])
    w2 = Word([98, 99, 100])
    print(lm.calculate(w1, w2))
