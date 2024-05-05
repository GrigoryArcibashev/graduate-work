class CalculatorLevenshteinMetricSettings:
    def __init__(self, raw_settings: dict):
        self._insert_cost = int(raw_settings['insert_cost'])
        self._delete_cost = int(raw_settings['delete_cost'])
        self._replace_cost = int(raw_settings['replace_cost'])

    @property
    def insert_cost(self) -> int:
        return self._insert_cost

    @property
    def delete_cost(self) -> int:
        return self._delete_cost

    @property
    def replace_cost(self) -> int:
        return self._replace_cost
