import hashlib
from typing import Iterator

from src.main.app.hasher.hash_alg import HashAlg
from src.main.app.settings.hash_settings import HashSettings


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
        if not isinstance(other, HashResult):
            raise TypeError(f'Operand type: expected {type(self)}, but actual is {type(other)}')
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


def main():
    hasher = Hasher(HashSettings({'algs': {'sha256': 'sha256'}, 'alg': 'sha256'}))
    message = "Hello, Python!".encode()

    def message2() -> Iterator[bytes]:
        msgs = ["Hello, ", "Python!"]
        for msg in msgs:
            yield msg.encode()

    h1 = hasher.calc_hash(message)
    h2 = hasher.calc_hash_by_iter(message2())
    print(h1 == h2)
    print(HashAlg.SHA256.to_str_name())


if __name__ == '__main__':
    main()
