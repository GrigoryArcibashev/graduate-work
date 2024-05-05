class ObfuscationDetSettings:
    def __init__(self, raw_settings: dict):
        self._obf_text_border = float(raw_settings['obf_text_border'])
        self._obf_name_border = float(raw_settings['obf_name_border'])
        self._max_non_obf_count_digits = int(raw_settings['max_non_obf_count_digits'])

    @property
    def obf_text_border(self) -> float:
        return self._obf_text_border

    @property
    def obf_name_border(self) -> float:
        return self._obf_name_border

    @property
    def max_non_obf_count_digits(self) -> int:
        return self._max_non_obf_count_digits
