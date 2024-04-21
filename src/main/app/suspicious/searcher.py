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
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W([\"\']cmd(?:\.exe)?[\"\'])\W', re.IGNORECASE),
            re.compile(br'\W([\"\']/bin/sh[\"\'])\W', re.IGNORECASE),
            re.compile(br'((?:web)?shell(?:exec)?)', re.IGNORECASE),
        ),
        DangerLevel.PAY_ATTENTION: (
            re.compile(br'[_\W](base_?(?:16|32|64|85))', re.IGNORECASE),
            re.compile(br'[_\W](rot_?13)', re.IGNORECASE),
        )
    },
    Language.PHP: {
        DangerLevel.DANGEROUS: (
            re.compile(br'[^\w\'\"]([Ee]val)(?:\s+[\'\"\w]|\s*\()'),

            re.compile(br'\W(passthru)\s*\('),
            re.compile(br'\W(proc_open)\s*\('),
            re.compile(br'[^\w\'\"](system)(?:\s+[\'\"\w]|\s*\()'),
        ),
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W(include(?:_once)?\s*\(.+?\))'),

            re.compile(br'\W(gzinflate)\s*\('),
            re.compile(br'\W(base64_(?:en|de)code)\s*\('),
            re.compile(br'\W(convert_uu(?:en|de)code)\s*\('),
            re.compile(br'\W(str_rot13)\s*\('),

            re.compile(br'\W([lf]?ch(?:grp|mod|own)(?:Sync|))\s*\('),
            re.compile(br'\W(file(?:_exists|_get_contents|_put_contents|inode|size|type|\?))\s*\('),
            re.compile(br'\W(f(?:cntl|open|passthru|read|scanf|[lr]?seek|(?:data)?sync|stat|write))\s*\('),
            re.compile(br'\W(dirname)\s*\('),
            re.compile(br'\W(is_?(?:dir|executable|file|link|readable|uploaded_file|write?able))\s*\('),
            re.compile(br'\W(mk(?:dirs?|node)(?:Sync|))\s*\('),
            re.compile(br'\W(move_uploaded_file)\s*\('),
            re.compile(br'\W(pathinfo)\s*\('),
            re.compile(br'\W(p(?:open|readv?|writev?|ipe))\s*\('),
            re.compile(br'\W(rm(?:dir|)(?:Sync|))\s*\('),

            re.compile(
                br'\W(eio_(?:f?ch(?:mod|own)|fallocate|'
                + br'ftruncate|init|link|mk(?:dir|nod)|open|'
                + br'read(?:dir|link)?|realpath|rmdir|'
                + br'seek|sendfile|write))\s*\('
            ),

            re.compile(br'\W(\$_FILES(?:\s*\[.+?])+)'),
        ),
        DangerLevel.PAY_ATTENTION: (
            re.compile(br'\W(require(?:_once)?\s*\(.+?\))'),

            re.compile(br'\W(\$_GET\s*\[.+?])'),
            re.compile(br'\W(\$_REQUEST\s*\[.+?])'),
        )
    },
    Language.JS: {
        DangerLevel.DANGEROUS: (
            re.compile(br'\W(document\s*\.\s*write)\s*\('),
            re.compile(br'\W(innerHTML)\s*\('),

            re.compile(br'[^\w\'\"]((?:shell_|pcntl_)?exec(?:File|[vl]p?e?|)(?:Sync|))(?:\s+[\'\"\w]|\s*\()'),
        ),
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W(atob)\s*\('),
            re.compile(br'\W(btoa)\s*\('),

            re.compile(br'\W(require\s*\(\s*[\"\'](?:fs|multer|express-fileupload|socket\.io)[\"\']\s*\))'),

            re.compile(br'\W(appendFile(?:Sync|))\s*\('),
            re.compile(br'\W(create(?:Read|Write)Stream)\s*\('),
            re.compile(br'\.(fd)\W'),
            re.compile(br'\W(read(?:v|dir|[Ff]ile|link|[Ll]ines?|partial|ableWebStream)(?:Sync|))\s*\('),
            re.compile(br'\W(write(?:v|File)(?:Sync|))\s*\('),
            re.compile(br'\W(open(?:dir|AsBlob)(?:Sync|))\s*\('),
        )
    },
    Language.PYTHON: {
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W((?:standard_|urlsafe_)?[ab](?:16|32|64|85)(?:hex)?(?:en|de)code)\s*\('),

            re.compile(br'\W(access)\s*\('),
            re.compile(br'\.(environb?)\W'),
            re.compile(br'\W(get(?:envb?|_exec_path))\s*\('),
            re.compile(br'\W(putenv)\s*\('),
            re.compile(br'\W(removedirs)\s*\('),
        ),
        DangerLevel.PAY_ATTENTION: (
            re.compile(br'(with\s+open\(.+?\)\s+as.+?:)'),
            re.compile(br'(=\s*open\(.+\))'),

            re.compile(br'\W(urllib\.urlretrieve)\s*\('),
            re.compile(br'\W(requests\.get)\s*\('),
        )
    },

    Language.RUBY: {
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W((?:strict_|urlsafe_)?(?:en|de)code64)\s*[({]'),

            re.compile(br'\W((?:re|sys)open)\s*\('),
            re.compile(br'\W(each_line)\s*[({]'),
            re.compile(br'\Wf(?:ile)?\s*\.\s*((?:write|read)(?:lines?)?)', re.IGNORECASE),

            re.compile(br'\W(directory\?)\s*\('),
            re.compile(br'\W((?:read|execut)able(?:_real)?\?)\s*\('),
        ),
        DangerLevel.PAY_ATTENTION: (
            re.compile(br'\W(Net\s*::\s*HTTP\s*\.\s*get(?:_response)?\s*\(.+\))'),
            re.compile(br'\W(http\s*\.\s*request(?:_get)?\s*\(.+\))'),
            re.compile(br'\W((?:popen|capture)(?:3|2e?))\s*\('),
        )
    },
    Language.C_SHARP: {
        DangerLevel.SUSPICIOUS: (
            re.compile(br'\W(FileStream)\W'),
            re.compile(br'\W(ICodeCompiler)\W'),
            re.compile(br'\W(CodeDom\.Compiler[.;])\W'),
            re.compile(br'\W(CodeAnalysis\.(?:CSharp\.)?Scripting[.;])\W'),
            re.compile(br'\W(CSharpScript\.(?:Run|Evaluate)Async)\W'),

            re.compile(br'\W(Download(?:Data|File|String)(?:(?:Task)?Async)?)\s*\('),
            re.compile(br'\W(FileMode\s*.\s*OpenOrCreate)\W'),

            re.compile(br'\W(DriveInfo)\W'),
            re.compile(br'\W(DirectoryInfo)\W'),
            re.compile(br'\W(Create(?:Subd|D)irectory|SymbolicLink)\s*\('),
            re.compile(br'\W(Enumerate(?:File(?:System(?:Infos)?|s)|Directories))\s*\('),
            re.compile(
                br'\W(Get(?:Drives|File(?:SystemEntries|s|)|(?:Current)?Directory|Directories))\s*\('
            ),
            re.compile(br'\W(Open(?:Read|Text|Write))\s*\('),
            re.compile(br'\W((?:Read|Write)All(?:Lines|Bytes|Text)(?:Async)?)\s*\('),
            re.compile(br'\W(ReadLines(?:Async)?)\s*\('),

            re.compile(br'\W((?:From|To)Base64(?:Transform|String|CharArray))\W'),
            re.compile(br'\W(SoapHexBinary)\W'),
        )
    }
}


def main():
    text = read_file('../../source/x.txt')
    # text = input().encode()
    pat_set = set()
    for lvl in DangerLevel:
        print(f'\n{"-" * (8 + len(lvl.name))}\n\t{lvl.name}\n{"-" * (8 + len(lvl.name))}')
        for lang in Language:
            if not (lang in PATTERNS and lvl in PATTERNS[lang]):
                continue
            for pat in PATTERNS[lang][lvl]:
                if pat in pat_set:
                    continue
                pat_set.add(pat)
                found = set(pat.findall(text))
                if found:
                    print(f'\n{pat}')
                    for fnd in found:
                        print(f'\t{fnd}')


if __name__ == '__main__':
    main()
