class CalculatorLevenshteinMetricSettings:
    def __init__(self):
        pass

    @property
    def insert_cost(self) -> int:
        pass

    @property
    def delete_cost(self) -> int:
        pass

    @property
    def replace_cost(self) -> int:
        pass
