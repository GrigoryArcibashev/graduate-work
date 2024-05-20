from enum import Enum


class HashAlg(Enum):
    SHA256 = 0
    MD5 = 1

    @staticmethod
    def make_from_str(alg_name: str):
        _alg_name = alg_name.strip().upper()
        if _alg_name == 'SHA256':
            return HashAlg.SHA256
        elif _alg_name == 'MD5':
            return HashAlg.MD5
        else:
            raise TypeError(f'Non-existent hash alg: {alg_name}')

    def to_str_name(self) -> str:
        return self.name
