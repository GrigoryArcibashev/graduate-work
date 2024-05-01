from src.main.app.encryption.encryption_determinator.encryption_determinants.abstract_encryption_determinator import \
    AbstractEncryptionDeterminator
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode, EncrVerdict
from src.main.app.encryption.entropy_analyzer import EntropyAnalyzer


class EncryptionDeterminatorByEntropy(AbstractEncryptionDeterminator):
    """
    Обнаруживает шифр в тексте путём расчёта энтропии
    """

    def __init__(self, entropy_analyzer: EntropyAnalyzer, mode: OperatingMode):
        super().__init__()
        self._entropy_analyzer = entropy_analyzer
        self._window_encryption_border = None
        self._unconditional_lower_bound_of_entropy = None
        self._conditional_lower_bound_of_entropy = None
        self._percent_of_entropy_vals_for_window = None
        self._upper_bound_of_entropy = None
        self.mode = mode

    def _set_boundaries(self, mode: OperatingMode) -> None:
        """
        Устанавливает граничные параметры для определения шифра,
        основываясь на режиме работы определителя

        :param mode: режим работы определителя

        :return: None
        """
        self._window_encryption_border = 60
        self._unconditional_lower_bound_of_entropy = 70
        self._conditional_lower_bound_of_entropy = 59
        self._percent_of_entropy_vals_for_window = 5
        if mode.is_strict:
            self._upper_bound_of_entropy = float('+inf')
        else:
            self._upper_bound_of_entropy = 95

    def determinate(self, data: list[int]) -> (EncrVerdict, float, float):
        """
        Рассчитывает энтропию текста и выносит вердикт (зашифрован/не зашифрован)

        :param data: текст в виде последовательности номеров байт

        :return: (вердикт, энтропия в целом, процент "окон" с энтропией выше установленной границы)
        """
        entropy = self._entropy_analyzer.analyze(data)
        entropies = self._entropy_analyzer.window_analyze(data)
        count_above_border = len(list(filter(lambda entr: entr >= self._window_encryption_border, entropies)))
        entropy_above_border = round(100 * count_above_border / len(entropies))
        return self._determinate(entropy, entropy_above_border), entropy, entropy_above_border

    def _determinate(self, entropy: float, entropy_above_border: float) -> EncrVerdict:
        """
        Выносит вердикт (EncrVerdict)

        :param entropy: энтропия в целом
        :param entropy_above_border: процент "окон" с энтропией выше установленной границы
        :return: вердикт (зашифрован/не зашифрован)
        """
        if entropy >= self._upper_bound_of_entropy:
            return EncrVerdict.NOT_DETECTED
        if (
                entropy >= self._unconditional_lower_bound_of_entropy
                or entropy >= self._conditional_lower_bound_of_entropy
                and entropy_above_border >= self._percent_of_entropy_vals_for_window
        ):
            return EncrVerdict.DETECTED
        return EncrVerdict.NOT_DETECTED
