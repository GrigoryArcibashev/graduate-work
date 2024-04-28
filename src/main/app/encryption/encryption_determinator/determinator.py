from src.main.app.encryption.encryption_determinator.encryption_determinants import EncryptionDeterminatorByHEX, \
    EncryptionDeterminatorByEntropy
from src.main.app.encryption.encryption_determinator.enums import OperatingMode, EncrVerdict
from src.main.app.encryption.encryption_filter import EncryptionFilter
from src.main.app.encryption.entropy_analyzer import EntropyAnalyzer, EntropyCalculator
from src.main.app.words_service.word_dict_service import WordDictService


class EncrAnalyzeResult:
    def __init__(
            self,
            hex_verdict: EncrVerdict,
            entr_verdict: EncrVerdict,
            cut_out_in_percent: float,
            entropy: float,
            entropy_above_border: float
    ):
        self._hex_verdict = hex_verdict
        self._entr_verdict = entr_verdict
        self._cut_out = cut_out_in_percent
        self._entropy = entropy
        self._entropy_above_border = entropy_above_border

    @property
    def hex_verdict(self) -> EncrVerdict:
        return self._hex_verdict

    @property
    def entr_verdict(self) -> EncrVerdict:
        return self._entr_verdict

    @property
    def cut_out_in_percent(self) -> float:
        return self._cut_out

    @property
    def entropy(self) -> float:
        return self._entropy

    @property
    def entropy_above_border(self) -> float:
        return self._entropy_above_border


class EncryptionDeterminator:
    def __init__(self, word_dict_service: WordDictService, mode: OperatingMode = OperatingMode.OPTIMAL):
        self._det_hex = EncryptionDeterminatorByHEX()
        self._det_ent = EncryptionDeterminatorByEntropy(EntropyAnalyzer(EntropyCalculator()))
        self._filter = EncryptionFilter(word_dict_service)
        self.mode = mode

    @property
    def mode(self) -> OperatingMode:
        return self._mode

    @mode.setter
    def mode(self, mode: OperatingMode) -> None:
        self._mode = mode
        self._det_hex.mode = mode
        self._det_ent.mode = mode

    def determinate(self, data: bytes) -> EncrAnalyzeResult:
        hex_verdict = self._det_hex.determinate(data)

        num_data = list(data)
        len_before = len(num_data)
        filtered_data = self._filter.filter(num_data)
        entr_verdict, entropy, entropy_above_border = self._det_ent.determinate(filtered_data)
        cut_out = round(100 * (len_before - len(filtered_data)) / len_before, 2)

        return EncrAnalyzeResult(hex_verdict, entr_verdict, cut_out, entropy, entropy_above_border)
