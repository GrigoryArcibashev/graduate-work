from src.main.app.model.encryption.encryption_determinator.encryption_determinants.abstract_encryption_determinator import \
    AbstractEncryptionDeterminator
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import EncrVerdict
from src.main.app.model.encryption.entropy_analyzer import EntropyAnalyzer
from src.main.app.model.settings.encr_entropy_settings import EncrDetEntropySettings


class EncryptionDeterminatorByEntropy(AbstractEncryptionDeterminator):
    """
    Обнаруживает шифр в тексте путём расчёта энтропии
    """

    def __init__(self, entropy_analyzer: EntropyAnalyzer, settings: EncrDetEntropySettings):
        super().__init__()
        self._entropy_analyzer = entropy_analyzer
        self._window_encryption_border = settings.window_encryption_border
        self._unconditional_lower_bound_of_entropy = settings.unconditional_lower_bound_of_entropy
        self._conditional_lower_bound_of_entropy = settings.conditional_lower_bound_of_entropy
        self._percent_of_entropy_vals_for_window = settings.percent_of_entropy_vals_for_window
        self._upper_bound_of_entropy_optimal = settings.upper_bound_of_entropy_optimal
        self._upper_bound_of_entropy_strict = settings.upper_bound_of_entropy_strict
        self.mode = settings.mode

    def determinate(self, data: list[int]) -> (EncrVerdict, float, float):
        """
        Рассчитывает энтропию текста и выносит вердикт (зашифрован/не зашифрован)

        :param data: текст в виде последовательности номеров байт

        :return: (вердикт, энтропия в целом, процент "окон" с энтропией выше установленной границы)
        """
        entropy = self._entropy_analyzer.analyze(data)
        entropies = self._entropy_analyzer.window_analyze(data)
        return self._make_result(entropies, entropy)

    def _make_result(self, entropies: list[float], entropy: float) -> (EncrVerdict, float, float):
        count_above_border = len(list(filter(lambda entr: entr >= self._window_encryption_border, entropies)))
        entropy_above_border = round(100 * count_above_border / len(entropies))
        return self._determinate(entropy, entropy_above_border), entropy, entropy_above_border

    @property
    def _upper_bound_of_entropy(self) -> float:
        """
        Устанавливает граничный параметр для обнаружения шифра,
        основываясь на режиме работы определителя

        :return: граничный параметр
        """
        return self._upper_bound_of_entropy_strict if self.mode.is_strict else self._upper_bound_of_entropy_optimal

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
