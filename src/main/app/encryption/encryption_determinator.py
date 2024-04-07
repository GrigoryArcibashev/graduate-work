import re


class EncryptionDeterminatorByHEX:
    """
    \x08
    0x4A
    0x54EF
    """

    def __init__(self):
        self._pattern = re.compile(br'(?:\\x|0x)[0-9AaBbCcDdEeFf]{2}', re.DOTALL)
        self._unicode_special = [
            ('\\xef', '\\xbb', '\\xbf'),  # utf8
            ('\\xff', '\\xfe'),  # utf16 LE
            ('\\xfe', '\\xff')  # utf16 BE
        ]

    def determinate(self, data):
        found = re.findall(self._pattern, data)
        count = len(self._filter_unicode(found))
        return count >= 5

    def _filter_unicode(self, found):
        for spec in self._unicode_special:
            len_sp = len(spec)
            if len_sp <= len(found) and spec == tuple(found[:len_sp]):
                return found[len_sp:]
        return found


class EncryptionDeterminatorByEntropy:
    def __init__(self, entropy_analyzer):
        self._entropy_analyzer = entropy_analyzer
        self._window_encryption_border = 60
        self._unconditional_lower_bound_of_entropy = 70
        self._conditional_lower_bound_of_entropy = 60
        self._percent_of_entropy_vals_for_window = 60

    def determinate(self, data):
        entropy = self._entropy_analyzer.analyze(data)
        entropies, window_size, hop = self._entropy_analyzer.window_analyze(data)
        count_above_border = len(list(filter(lambda entr: entr >= self._window_encryption_border, entropies)))
        entropy_above_border = round(100 * count_above_border / len(entropies))
        return self._is_encr(entropy, entropy_above_border), entropy, entropy_above_border

    def _is_encr(self, entropy, entropy_above_border):
        return (
                entropy >= self._unconditional_lower_bound_of_entropy
                or entropy >= self._conditional_lower_bound_of_entropy
                and entropy_above_border >= self._percent_of_entropy_vals_for_window
        )


def main():
    det = EncryptionDeterminatorByHEX()
    string = br'0xFF0xA3\\x32\\x430x33'
    print(det.determinate(string))


if __name__ == '__main__':
    main()
