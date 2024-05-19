class HashResult:
    def __init__(self, _hash: str):
        self._hash = _hash

    def hash(self) -> str:
        return self._hash

    def __str__(self):
        return str(self._hash)
