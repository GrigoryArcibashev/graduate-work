class EntropyAnalyzerSettings:
    def __init__(self, raw_settings: dict):
        self._min_window_size = int(raw_settings['min_window_size'])
        self._min_hope = int(raw_settings['min_hope'])
        self._divider_for_window = int(raw_settings['divider_for_window'])
        self._divider_for_hop = int(raw_settings['divider_for_hop'])

    @property
    def min_window_size(self) -> int:
        return self._min_window_size

    @property
    def min_hope(self) -> int:
        return self._min_hope

    @property
    def divider_for_window(self) -> int:
        return self._divider_for_window

    @property
    def divider_for_hop(self) -> int:
        return self._divider_for_hop
