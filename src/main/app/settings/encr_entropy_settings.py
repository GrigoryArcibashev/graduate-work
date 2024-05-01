from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode


class EncrDetEntropySettings:
    def __init__(self):
        pass

    def mode(self) -> OperatingMode:
        pass

    def window_encryption_border(self) -> float:
        pass

    def unconditional_lower_bound_of_entropy(self) -> float:
        pass

    def conditional_lower_bound_of_entropy(self) -> float:
        pass

    def percent_of_entropy_vals_for_window(self) -> float:
        pass

    def upper_bound_of_entropy_optimal(self) -> float:
        pass

    def upper_bound_of_entropy_strict(self) -> float:
        pass
