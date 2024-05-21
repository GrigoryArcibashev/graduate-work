from glob import glob
from os.path import isfile
from typing import Iterator


class FileExplorer:
    @staticmethod
    def get_all_filenames(root: str, recursive: bool = False) -> Iterator[str]:
        root += '/**/*' if root[-1] != '/' else '**/*'
        for filename in glob(root + '', recursive=recursive):
            if isfile(filename):
                yield filename


if __name__ == '__main__':
    c = 0
    for fn in FileExplorer.get_all_filenames('../../source/', recursive=True):
        c += 1
        print(f'{c}. {fn}')
