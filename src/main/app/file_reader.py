import pickle
from typing import Any


def read_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


def read_file_by_pickle(path: str) -> Any:
    with open(path, 'rb') as f:
        return pickle.load(f)
