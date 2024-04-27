from src.main.app.encryption.encryption_determinator.determinator import EncrAnalyzeResult
from src.main.app.obfuscation.obfuscation_determinator import ObfuscationResult
from src.main.app.suspicious.suspicious_code import SuspiciousCode


class AnalysisResult:
    def __init__(self, encr_res: EncrAnalyzeResult, obf_res: ObfuscationResult, suspy_res: list[SuspiciousCode]):
        self._encr_res = encr_res
        self._obf_res = obf_res
        self._suspy_res = suspy_res

    @property
    def encr_res(self) -> EncrAnalyzeResult:
        return self._encr_res

    @property
    def obf_res(self) -> ObfuscationResult:
        return self._obf_res

    @property
    def suspy_res(self) -> list[SuspiciousCode]:
        return self._suspy_res

    def __str__(self):
        return self.to_str()

    def to_str(self) -> str:
        return self._encr_res_to_str() + self._obf_res_to_str() + self._suspy_res_to_str()

    def _encr_res_to_str(self) -> str:
        result = ['ПОИСК ШИФРА', ]
        if self.encr_res.entr_verdict.is_encr or self.encr_res.hex_verdict.is_encr:
            result.append(f'\tЕСТЬ ШИФР')
        else:
            result.append('\tНЕТ ШИФРА')
        if self.encr_res.entr_verdict.is_encr:
            result.append(f'\t  +Энтропия ({self.encr_res.entr_verdict.to_str()})')
            result.append(f'\t\t(энт. {self.encr_res.entropy}% | {self.encr_res.entropy_above_border}%)')
            result.append(f'\t\t(выр. {self.encr_res.cut_out_in_percent}%)')
        if self.encr_res.hex_verdict.is_encr:
            result.append(f'\t  +HEX ({self.encr_res.hex_verdict.to_str()})')
        return '\n'.join(result) + '\n'

    def _obf_res_to_str(self) -> str:
        result = ['\nПОИСК ОБФУСКАЦИИ', ]
        if self.obf_res.is_obf:
            result.append(
                f'\tОБНАРУЖЕНА ({self.obf_res.proportion_of_obf_names} > {self.obf_res.max_allowable_proportion})'
            )
        else:
            result.append(f'\tНЕТ ({self.obf_res.proportion_of_obf_names} <= {self.obf_res.max_allowable_proportion})')
        return '\n'.join(result) + '\n'

    def _suspy_res_to_str(self) -> str:
        result = ['\nПОИСК ПОДОЗРИТЕЛЬНЫХ КОМАНД', ]
        if not self.suspy_res:
            result.append('\tНЕ НАЙДЕНО')
        else:
            for suspy in self.suspy_res:
                result.append(f'\t{suspy}')
        return '\n'.join(result) + '\n'
