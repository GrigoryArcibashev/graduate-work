import re
from enum import Enum

from src.main.app.file_reader import read_file


class DangerLevel(Enum):
    DANGEROUS = 0
    SUSPICIOUS = 1
    PAY_ATTENTION = 2


class Language(Enum):
    GENERAL = 0,
    PHP = 1,
    JS = 2
    PYTHON = 3
    RUBY = 4
    C_SHARP = 5


PATTERNS = {
    Language.GENERAL: {  # TODO команды cmd bash
        DangerLevel.DANGEROUS: (
            re.compile(br'\W([\"\']cmd(?:\.exe)?[\"\'])\W', re.IGNORECASE),
            re.compile(br'(webshell)', re.IGNORECASE),
        ),
        DangerLevel.SUSPICIOUS: (
            re.compile(br'[_\W](base_?(?:64|32|85))', re.IGNORECASE),
            re.compile(br'[_\W](rot_?13)', re.IGNORECASE),
        )
    },
    Language.PHP: {
        DangerLevel.DANGEROUS: (
            re.compile(br'\W(eval)\s*\('),

            re.compile(br'\W(passthru)\s*\('),
            re.compile(br'\W(proc_open)\s*\('),
            re.compile(br'\W(system)\s*\('),
        ),
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W(include(?:_once)?\s*\(.+?\))'),
            re.compile(br'\W(require(?:_once)?\s*\(.+?\))'),

            re.compile(br'\W(gzinflate)\s*\('),
            re.compile(br'\W(base64_(?:en|de)code)\s*\('),
            re.compile(br'\W(convert_uu(?:en|de)code)\s*\('),
            re.compile(br'\W(str_rot13)\s*\('),

            re.compile(br'\W([lf]?ch(?:grp|mod|own)(?:Sync|))\s*\('),
            re.compile(br'\W(file(?:_exists|_get_contents|_put_contents|inode|size|type)?)\s*\('),
            re.compile(br'\W(f(?:eof|lock|open|passthru|read|scanf|seek|sync|write))\s*\('),
            re.compile(br'\W(dirname)\s*\('),
            re.compile(br'\W(is_(?:dir|executable|file|link|readable|uploaded_file|write?able))\s*\('),
            re.compile(br'\W(mkdir(?:Sync|))\s*\('),
            re.compile(br'\W(move_uploaded_file)\s*\('),
            re.compile(br'\W(pathinfo)\s*\('),
            re.compile(br'\W(popen)\s*\('),
            re.compile(br'\W(rm(?:dir|)(?:Sync|))\s*\('),

            re.compile(
                br'\W(eio_(?:f?ch(?:mod|own)|fallocate|'
                + br'ftruncate|init|link|mk(?:dir|nod)|open|'
                + br'read(?:dir|link)?|realpath|rmdir|'
                + br'seek|sendfile|write))\s*\('
            )
        ),
        DangerLevel.PAY_ATTENTION: (
            re.compile(br'\W(\$_GET\s*\[.+?])'),
            re.compile(br'\W(\$_POST\s*\[.+?])'),
            re.compile(br'\W(\$_REQUEST\s*\[.+?])'),
        )
    },
    Language.JS: {
        DangerLevel.DANGEROUS: (
            re.compile(br'\W(document\s*\.\s*write)\s*\('),
            re.compile(br'\W(innerHTML)\s*\('),

            re.compile(br'\W((?:shell_|pcntl_)?exec(?:File|)(?:Sync|))\s*\('),
        ),
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W(atob)\s*\('),
            re.compile(br'\W(btoa)\s*\('),

            re.compile(br'\W(appendFile(?:Sync|))\s*\('),
            re.compile(br'\W(create(?:Read|Write)Stream)\s*\('),
            re.compile(br'\.(fd)\W'),
            re.compile(br'\W(read(?:v|dir|[Ff]ile|link|Lines|ableWebStream)(?:Sync|))\s*\('),
            re.compile(br'\W(write(?:v|File)(?:Sync|))\s*\('),
            re.compile(br'\W(open(?:dir|AsBlob)(?:Sync|))\s*\('),

        )
    }
}


def main():
    text = read_file('../../source/x.txt')
    # text = input().encode()
    pat_set = set()
    for lang in Language:
        for lvl in DangerLevel:
            for pat in PATTERNS[lang][lvl]:
                if pat in pat_set:
                    continue
                pat_set.add(pat)
                found = pat.findall(text)
                if found:
                    print(pat)
                    print(found, end='\n\n')


if __name__ == '__main__':
    main()
