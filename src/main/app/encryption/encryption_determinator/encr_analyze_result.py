from src.main.app.encryption.encryption_determinator.enums import EncrVerdict


class EncrAnalyzeResult:
    """
    Результат работы обнаружителя шифров
    """

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
        """
        Результат работы обнаружителя HEX

        :return: вердикт
        """
        return self._hex_verdict

    @property
    def entr_verdict(self) -> EncrVerdict:
        """
        Результат работы обнаружителя шифров на основе энтропии

        :return: вердикт
        """
        return self._entr_verdict

    @property
    def cut_out_in_percent(self) -> float:
        """
        Сколько было вырезано из текста в процессе анализа (отладочная информация)

        :return: процент вырезанных символов (с двумя знаками после запятой)
        """
        return self._cut_out

    @property
    def entropy_in_percent(self) -> float:
        """
        Энтропия в целом в процентах

        :return: энтропия в целом в процентах (с двумя знаками после запятой)
        """
        return self._entropy

    @property
    def entropy_above_border_in_percent(self) -> float:
        """
        Процент "окон" с энтропией выше установленной границы

        :return: процент "окон" с энтропией выше установленной границы (с двумя знаками после запятой)
        """
        return self._entropy_above_border
