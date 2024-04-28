from src.main.app.encryption.encryption_determinator.encr_analyze_result import EncrAnalyzeResult
from src.main.app.encryption.encryption_determinator.encryption_determinants.encryption_determinator_entropy import \
    EncryptionDeterminatorByEntropy
from src.main.app.encryption.encryption_determinator.encryption_determinants.encryption_determinator_hex import \
    EncryptionDeterminatorByHEX
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode
from src.main.app.encryption.encryption_filter import EncryptionFilter
from src.main.app.encryption.entropy_analyzer import EntropyAnalyzer, EntropyCalculator
from src.main.app.words_service.word_dict_service import WordDictService


class EncryptionDeterminator:
    def __init__(self, word_dict_service: WordDictService, mode: OperatingMode = OperatingMode.OPTIMAL):
        self._det_hex = EncryptionDeterminatorByHEX()
        self._det_ent = EncryptionDeterminatorByEntropy(EntropyAnalyzer(EntropyCalculator()))
        self._filter = EncryptionFilter(word_dict_service)
        self.mode = mode

    @property
    def mode(self) -> OperatingMode:
        """
        Возвращает режим работы определителя

        :return: режим работы определителя
        """
        return self._mode

    @mode.setter
    def mode(self, mode: OperatingMode) -> None:
        """
        Устанавливает режим работы определителя

        :param mode: режим работы определителя
        :return: None
        """
        self._mode = mode
        self._det_hex.mode = mode
        self._det_ent.mode = mode

    def determinate(self, data: bytes) -> EncrAnalyzeResult:
        """
        Определяет, есть ли в тексте шифр

        :param data: текст
        :return: EncrAnalyzeResult
        """
        hex_verdict = self._det_hex.determinate(data)

        num_data = list(data)
        len_before = len(num_data)
        filtered_data = self._filter.filter(num_data)
        entr_verdict, entropy, entropy_above_border = self._det_ent.determinate(filtered_data)
        cut_out = round(100 * (len_before - len(filtered_data)) / len_before, 2)

        return EncrAnalyzeResult(hex_verdict, entr_verdict, cut_out, entropy, entropy_above_border)
