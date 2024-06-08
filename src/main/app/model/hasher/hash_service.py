import hashlib
from typing import Iterator

from src.main.app.model.hasher.hash_alg import HashAlg
from src.main.app.model.settings.hash_settings import HashSettings


class HashResult:
    def __init__(self, _hash: str):
        self._hash = _hash

    def hash(self) -> str:
        return self._hash

    def __str__(self):
        return str(self._hash)

    def __hash__(self):
        return hash(self._hash)

    def __eq__(self, other):
        if other is None or not isinstance(other, HashResult):
            return False
        return self._hash == other._hash


class Hasher:
    def __init__(self, settings: HashSettings):
        self._hash_func_name = settings.hash_alg.to_str_name()

    def calc_hash(self, data: bytes) -> HashResult:
        _hash = hashlib.new(self._hash_func_name)
        _hash.update(data)
        return HashResult(_hash.hexdigest())

    def calc_hash_by_iter(self, data_iter: Iterator[bytes]) -> HashResult:
        _hash = hashlib.new(self._hash_func_name)
        for data in data_iter:
            _hash.update(data)
        return HashResult(_hash.hexdigest())
