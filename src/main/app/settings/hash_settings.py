from src.main.app.hasher.hash_alg import HashAlg


class HashSettings:
    def __init__(self, raw_settings: dict):
        alg_name = str(raw_settings['algs'][raw_settings['alg']])
        self._alg = HashAlg.make_from_str(alg_name)

    @property
    def hash_alg(self) -> HashAlg:
        return self._alg
