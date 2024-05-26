from src.main.app.model.encryption.encryption_determinator.encr_analyze_result import EncrAnalyzeResult
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.encryption_determinator_entropy import EncryptionDeterminatorByEntropy
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.encr_determinator_hex.encryption_determinator_hex import EncryptionDeterminatorByHEX
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode
from src.main.app.model.encryption.encryption_filter import EncryptionFilter
from src.main.app.model.encryption.entropy_analyzer import EntropyAnalyzer, EntropyCalculator
from src.main.app.model.settings.encr_entropy_settings import EncrDetEntropySettings
from src.main.app.model.settings.encr_filter_settings import EncrFilterSettings
from src.main.app.model.settings.encr_hex_settings import EncrDetHEXSettings
from src.main.app.model.settings.entropy_analyzer_settings import EntropyAnalyzerSettings
from src.main.app.model.words_service.word_dict_service import WordDictService


class EncryptionDeterminator:
    def __init__(
            self,
            word_dict_service: WordDictService,
            entropy_det_settings: EncrDetEntropySettings,
            hex_det_settings: EncrDetHEXSettings,
            entropy_analyzer_settings: EntropyAnalyzerSettings,
            encr_filter_settings: EncrFilterSettings
    ):
        self._det_hex = EncryptionDeterminatorByHEX(hex_det_settings)
        self._det_ent = EncryptionDeterminatorByEntropy(
            EntropyAnalyzer(EntropyCalculator(), entropy_analyzer_settings),
            entropy_det_settings
        )
        self._filter = EncryptionFilter(word_dict_service, encr_filter_settings)
        self.hex_mode = entropy_det_settings.mode
        self.entr_mode = hex_det_settings.mode

    @property
    def hex_mode(self) -> OperatingMode:
        """
        Возвращает режим работы обнаружителя HEX

        :return: режим работы обнаружителя
        """
        return self._det_hex.mode

    @hex_mode.setter
    def hex_mode(self, mode: OperatingMode) -> None:
        """
        Устанавливает режим работы обнаружителя HEX

        :param mode: режим работы обнаружителя
        :return: None
        """
        self._det_hex.mode = mode

    @property
    def entr_mode(self) -> OperatingMode:
        """
        Возвращает режим работы обнаружителя высокой энтропии

        :return: режим работы обнаружителя
        """
        return self._det_ent.mode

    @entr_mode.setter
    def entr_mode(self, mode: OperatingMode) -> None:
        """
        Устанавливает режим работы обнаружителя высокой энтропии

        :param mode: режим работы обнаружителя

        :return: None
        """
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
        cut_out = round(100 * (len_before - len(filtered_data)) / max(1, len_before), 2)

        return EncrAnalyzeResult(hex_verdict, entr_verdict, cut_out, entropy, entropy_above_border)
