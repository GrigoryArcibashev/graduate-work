class EncryptionDeterminator:
    def __init__(self, entropy_analyzer):
        self._entropy_analyzer = entropy_analyzer
        self._window_encryption_border = 60
        self._unconditional_lower_bound_of_entropy = 70
        self._conditional_lower_bound_of_entropy = 65
        self._percent_of_entropy_vals_for_window = 55

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
