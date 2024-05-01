from src.main.app.words_service.word_dict_service import WordDictService
from src.main.app.extractors.token import TokenType, Token
from src.main.app.extractors.token_extractor import TokenExtractor
from src.main.app.extractors.word_extractor import WordExtractor


class EncryptionFilter:
    """
    Находит и удаляет незашифрованную часть текста
    """

    def __init__(self, word_dict_service: WordDictService):
        self._word_dict_service = word_dict_service
        self._token_extractor = TokenExtractor()
        self._word_extractor = WordExtractor()
        self._encryption_boundary = 0.5
        self._save_del_size = 0.5

    def filter(self, data: list[int]) -> list[int]:
        """
        Фильтрует текст: находит и удаляет незашифрованную часть текста

        :param data: текст в виде последовательности номеров байт
        :return: "отфильтрованный" текст в виде последовательности номеров байт
        """
        result = list()
        prev_let_token_is_encr = True
        current_non_letter_tokens = list()
        for token in self._token_extractor.get_token_iter(data):
            if token.type == TokenType.LETTERS:
                extend, prev_let_token_is_encr = self.process_letter_token(
                    token,
                    current_non_letter_tokens,
                    prev_let_token_is_encr
                )
                result.extend(extend)
                current_non_letter_tokens.clear()
            else:
                current_non_letter_tokens.append(token)
        result.extend(current_non_letter_tokens)
        return self.map_tokens_to_bytes(result)

    def process_letter_token(
            self,
            token: Token,
            current_non_letter_tokens: list[Token],
            prev_let_token_is_encr: bool
    ) -> (list[Token], bool):
        """
        Основываясь на ранее считанные символы и значение очередного буквенного
        токена определяет, какие токены будут сохранены, а какие вырезаны

        :param token: очередной буквенный токен (TokenType.LETTERS)
        :param current_non_letter_tokens: все небуквенные токены
        между последним буквенным и текущим

        :param prev_let_token_is_encr: было ли значение последнего
        токена шифром (да-True, нет-False)
        :return: все сохраненные символы из current_non_letter_tokens
        между буквенными токенами и сам токен, если его значение
        было признано зашифрованным
        """
        res = list()
        if self.is_letter_token_encr(token):
            if prev_let_token_is_encr:  # encr _ encr
                res.extend(current_non_letter_tokens)
            elif len(current_non_letter_tokens) > 1:  # non _ encr
                half = current_non_letter_tokens[int(len(current_non_letter_tokens) * self._save_del_size):]
                res.extend(half)
            res.append(token)
            is_encr = True
        else:
            if prev_let_token_is_encr and len(current_non_letter_tokens) > 1:  # encr _ non
                half = current_non_letter_tokens[:int(len(current_non_letter_tokens) * self._save_del_size)]
                res.extend(half)
            is_encr = False
        return res, is_encr

    def is_letter_token_encr(self, token: Token) -> bool:
        """
        Определяет, является ли значение буквенного токена зашифрованным

        :param token: буквенный токен (TokenType.LETTERS)
        :return: True, если значение зашифровано, иначе - False
        """
        good_count = 0
        for word in self._word_extractor.get_word_iter(token.value):
            if self._word_dict_service.check_word(word):
                good_count += len(word)
        return good_count / len(token) < self._encryption_boundary

    @staticmethod
    def map_tokens_to_bytes(tokens: list[Token]) -> list[int]:
        """
        Переводит последовательность токенов в последовательность их значений в виде номеров байт

        :param tokens: последовательность токенов

        :return: последовательность значений токенов в виде номеров байт
        """
        result = list()
        for token in tokens:
            result.extend(token.value)
        return result
