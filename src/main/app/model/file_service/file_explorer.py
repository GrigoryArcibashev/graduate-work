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
