from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import OperatingMode


class EncrDetHEXSettings:
    def __init__(self):
        pass

    @property
    def mode(self) -> OperatingMode:
        pass

    @property
    def min_count_optimal(self) -> int:
        pass

    @property
    def min_count_strict(self) -> int:
        pass
