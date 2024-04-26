import re

from src.main.app.encryption.entropy.entropy_analyzer import EntropyAnalyzer
from src.main.app.encryption.encryption_determinator.enums import OperatingMode, EncrVerdict


class EncryptionDeterminatorByHEX:
    def __init__(self, mode: OperatingMode):
        self._set_boundaries(mode)
        self._pattern = re.compile(br'(?:\\x|0x|\\u)[0-9abcdef]{2}', re.IGNORECASE)
        self._unicode_markers = [
            (br'\xef', br'\xbb', br'\xbf'),  # UTF8
            (br'0xef', br'0xbb', br'0xbf'),
            (br'\xff', br'\xfe'),  # UTF16 LE
            (br'0xff', br'0xfe'),
            (br'\xfe', br'\xff'),  # UTF16 BE
            (br'0xfe', br'0xff'),
            (br'\xff', br'\xfe', br'\x00', br'\x00'),  # UTF32 LE
            (br'0xff', br'0xfe', br'0x00', br'0x00'),
            (br'\x00', br'\x00', br'\xfe', br'\xff'),  # UTF32 BE
            (br'0x00', br'0x00', br'0xfe', br'0xff'),
            (br'\x2b', br'\x2f', br'\x76', br'\x38'),  # UTF7 (1)
            (br'0x2b', br'0x2f', br'0x76', br'0x38'),
            (br'\x2b', br'\x2f', br'\x76', br'\x39'),  # UTF7 (2)
            (br'0x2b', br'0x2f', br'0x76', br'0x39'),
            (br'\x2b', br'\x2f', br'\x76', br'\x2b'),  # UTF7 (3)
            (br'0x2b', br'0x2f', br'0x76', br'0x2b'),
            (br'\x2b', br'\x2f', br'\x76', br'\x2f'),  # UTF7 (4)
            (br'0x2b', br'0x2f', br'0x76', br'0x2f'),
            (br'\xf7', br'\x64', br'\x4c'),  # UTF1
            (br'0xf7', br'0x64', br'0x4c'),
            (br'\xdd', br'\x73', br'\x66', br'\x73'),  # UTF-EBCDIC
            (br'0xdd', br'0x73', br'0x66', br'0x73')
        ]

    def _set_boundaries(self, mode: OperatingMode) -> None:
        if mode == OperatingMode.OPTIMAL:
            self._min_count = 10
        elif mode.is_strict:
            self._min_count = 3
        else:
            raise NotImplementedError(f'{mode} is not supported')
        self._ext_count = 2 * self._min_count

    def determinate(self, data: bytes) -> EncrVerdict:
        found = re.findall(self._pattern, data)
        count = len(self._filter_unicode(found))
        if count > self._ext_count:
            return EncrVerdict.EXTREMELY_LIKELY
        if count > self._min_count:
            return EncrVerdict.LIKELY
        return EncrVerdict.UNLIKELY

    def _filter_unicode(self, found) -> list:
        for marker in self._unicode_markers:
            len_mkr = len(marker)
            if len_mkr <= len(found) and self._hex_eq(marker, found[:len_mkr]):
                return found[len_mkr:]
        return found

    @staticmethod
    def _hex_eq(hex1, hex2) -> bool:
        if len(hex1) != len(hex2):
            return False
        for i in range(len(hex1)):
            if hex1[i].lower() != hex2[i].lower():
                return False
        return True


class EncryptionDeterminatorByEntropy:
    def __init__(
            self,
            entropy_analyzer: EntropyAnalyzer,
            mode: OperatingMode,
            web, ulboe, clboe, poevfw):
        self._entropy_analyzer = entropy_analyzer
        self._set_boundaries(mode, web, ulboe, clboe, poevfw)

    def _set_boundaries(self, mode: OperatingMode, web, ulboe, clboe, poevfw) -> None:
        #############
        self._window_encryption_border = web
        self._unconditional_lower_bound_of_entropy = ulboe
        self._conditional_lower_bound_of_entropy = clboe
        self._percent_of_entropy_vals_for_window = poevfw
        #############

        # if mode == OperatingMode.OPTIMAL:
        #     self._window_encryption_border = 60
        #     self._unconditional_lower_bound_of_entropy = 70
        #     self._conditional_lower_bound_of_entropy = 60
        #     self._percent_of_entropy_vals_for_window = 60
        # elif mode.is_strict:
        #     self._window_encryption_border = 57
        #     self._unconditional_lower_bound_of_entropy = 65
        #     self._conditional_lower_bound_of_entropy = 55
        #     self._percent_of_entropy_vals_for_window = 70

        if mode == OperatingMode.OPTIMAL or mode == OperatingMode.LOWER_STRICT:
            self._upper_bound_of_entropy = 95
        elif mode == OperatingMode.STRICT:
            self._upper_bound_of_entropy = float('+inf')
        else:
            raise NotImplementedError(f'{mode} is not supported')

    def determinate(self, data) -> (EncrVerdict, float, float):
        entropy = self._entropy_analyzer.analyze(data)
        entropies, window_size, hop = self._entropy_analyzer.window_analyze(data)
        count_above_border = len(list(filter(lambda entr: entr >= self._window_encryption_border, entropies)))
        entropy_above_border = round(100 * count_above_border / len(entropies))
        return self._determinate(entropy, entropy_above_border), entropy, entropy_above_border

    def _determinate(self, entropy, entropy_above_border) -> EncrVerdict:
        if entropy >= self._upper_bound_of_entropy:
            return EncrVerdict.UNLIKELY
        if entropy >= self._unconditional_lower_bound_of_entropy:
            return EncrVerdict.EXTREMELY_LIKELY
        if (
                entropy >= self._conditional_lower_bound_of_entropy
                and entropy_above_border >= self._percent_of_entropy_vals_for_window
        ):
            return EncrVerdict.LIKELY
        return EncrVerdict.UNLIKELY
