class EntropyAnalyzer:
    def __init__(self, entropy):
        self._entropy = entropy
        self._min_window_size = 100
        self._min_hope = 1

    def window_analyze(self, data, window_size=None, hop=None):
        if window_size is None:
            window_size = min(max(len(data) // 200, self._min_window_size), len(data))
        if hop is None:
            hop = max(window_size // 15, self._min_hope)
        shift = 0
        limit = len(data)
        entropies = []
        while shift + window_size <= limit:
            window = data[shift: shift + window_size]
            entropies.append(self.analyze(window))
            shift += hop
        return entropies, window_size, hop

    def analyze(self, data):
        return self._entropy.calc_entropy_in_percent(data)
