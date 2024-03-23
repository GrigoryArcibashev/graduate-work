class EntropyAnalyzer:
    def __init__(self, entropy_calculator):
        self._entropy_calculator = entropy_calculator
        self._min_window_size = 100
        self._min_hope = 1
        self._divider_for_window = 120
        self._divider_for_hop = 5

    def analyze(self, data):
        return self._entropy_calculator.calc_entropy_in_percent(data)

    def window_analyze(self, data):
        window_size = self._calc_window_size(data)
        hop = self._calc_hop_size(window_size)
        shift = 0
        limit = len(data)
        entropies = []
        while shift + window_size <= limit:
            window = data[shift: shift + window_size]
            entropies.append(self.analyze(window))
            shift += hop
        return entropies, window_size, hop

    def _calc_hop_size(self, window_size):
        hop = window_size // self._divider_for_hop
        return max(hop, self._min_hope)

    def _calc_window_size(self, data):
        window_size = len(data) // self._divider_for_window
        return min(max(window_size, self._min_window_size), len(data))
