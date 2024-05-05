from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode


class EncrDetHEXSettings:
    def __init__(self, raw_settings: dict, modes: dict):
        self._mode = OperatingMode.make_from_str(modes[raw_settings['mode']])
        self._min_count_optimal = int(raw_settings['min_count_optimal'])
        self._min_count_strict = int(raw_settings['min_count_strict'])

    @property
    def mode(self) -> OperatingMode:
        return self._mode

    @property
    def min_count_optimal(self) -> int:
        return self._min_count_optimal

    @property
    def min_count_strict(self) -> int:
        return self._min_count_strict
