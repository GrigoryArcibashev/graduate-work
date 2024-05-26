import json
import pickle
from typing import Any, Iterator


class FileReader:
    @staticmethod
    def read_file_by_iter(path: str, buffer_size: int) -> Iterator[bytes]:
        with open(path, 'rb') as f:
            read = f.read(buffer_size)
            while read:
                yield read
                read = f.read(buffer_size)

    @staticmethod
    def read_file(path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def read_file_by_pickle(path: str) -> Any:
        with open(path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def read_json(path: str) -> Any:
        with open(path, 'r') as f:
            return json.load(f)
