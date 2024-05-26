class EncrFilterSettings:
    def __init__(self, raw_settings: dict):
        self._encryption_boundary = float(raw_settings['encryption_boundary'])
        self._save_del_size = float(raw_settings['save_del_size'])

    @property
    def encryption_boundary(self) -> float:
        return self._encryption_boundary

    @property
    def save_del_size(self) -> float:
        return self._save_del_size
