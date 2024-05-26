class SearcherLevenshteinMetricSettings:
    def __init__(self, raw_settings: dict):
        self._mult_for_max_lev_distance = float(raw_settings['mult_for_max_lev_distance'])

    @property
    def mult_for_max_lev_distance(self) -> float:
        return self._mult_for_max_lev_distance
