from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode


class EncrDetEntropySettings:
    def __init__(self, raw_settings: dict, modes: dict):
        self._mode = OperatingMode.make_from_str(modes[raw_settings['mode']])
        self._window_encryption_border = float(raw_settings['window_encryption_border'])
        self._unconditional_lower_bound_of_entropy = float(raw_settings['unconditional_lower_bound_of_entropy'])
        self._conditional_lower_bound_of_entropy = float(raw_settings['conditional_lower_bound_of_entropy'])
        self._percent_of_entropy_vals_for_window = float(raw_settings['percent_of_entropy_vals_for_window'])
        self._upper_bound_of_entropy_optimal = float(raw_settings['upper_bound_of_entropy_optimal'])
        self._upper_bound_of_entropy_strict = float(raw_settings['upper_bound_of_entropy_strict'])

    @property
    def mode(self) -> OperatingMode:
        return self._mode

    @property
    def window_encryption_border(self) -> float:
        return self._window_encryption_border

    @property
    def unconditional_lower_bound_of_entropy(self) -> float:
        return self._unconditional_lower_bound_of_entropy

    @property
    def conditional_lower_bound_of_entropy(self) -> float:
        return self._conditional_lower_bound_of_entropy

    @property
    def percent_of_entropy_vals_for_window(self) -> float:
        return self._percent_of_entropy_vals_for_window

    @property
    def upper_bound_of_entropy_optimal(self) -> float:
        return self._upper_bound_of_entropy_optimal

    @property
    def upper_bound_of_entropy_strict(self) -> float:
        return self._upper_bound_of_entropy_strict
