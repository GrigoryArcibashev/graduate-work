import re
from typing import Iterator

from src.main.app.file_reader import read_file
from src.main.app.suspicious.enums import DangerLevel, SuspiciousType
from src.main.app.suspicious.suspicious_code import SuspiciousCode


class PatternContainer:
    def __init__(self, pattern: re.Pattern, danger_lvl: DangerLevel, code_type: SuspiciousType):
        self.pattern = pattern
        self.danger_lvl = danger_lvl
        self.type = code_type

    def __str__(self):
        return f'{self.danger_lvl} => {self.type} => {self.pattern}'


class SuspySearcher:

    def __init__(self):
        self._patterns = {
            DangerLevel.DANGEROUS: {
                SuspiciousType.EXECUTION: {
                    re.compile(br'[^\w\'\"]([Ee]val)(?:\s+[\'\"\w]|\s*\()'),
                    re.compile(br'\W(passthru)\s*\('),
                    re.compile(br'\W(proc_open)\s*\('),
                    re.compile(br'[^\w\'\"](system)(?:\s+[\'\"\w]|\s*\()'),
                    re.compile(br'[^\w\'\"]((?:shell_|pcntl_)?exec(?:File|[vl]p?e?|)(?:Sync|))(?:\s+[\'\"\w]|\s*\()'),
                    re.compile(br'\W(ICodeCompiler)\W'),
                    re.compile(br'\W(CodeDom\.Compiler[.;])\W'),
                    re.compile(br'\W(CodeAnalysis\.(?:CSharp\.)?Scripting[.;])\W'),
                    re.compile(br'\W(CSharpScript\.(?:Run|Evaluate)Async)\W'),
                    re.compile(br'\W(innerHTML)\s*\('),
                },
            },
            DangerLevel.SUSPICIOUS: {
                SuspiciousType.GENERAL: {
                    re.compile(br'[_\W](rot_?(?:5|13|18|47))', re.IGNORECASE),
                    re.compile(
                        br'[_\W]((?:ascii|base|radix)_?(?:16|32|36|45|56|58|62|64|85|91|94|122|xml)_?(?:hex|url)?)',
                        re.IGNORECASE
                    ),
                },
                SuspiciousType.COMMAND: {
                    re.compile(
                        br'\W([\"\'] *'
                        + br'(?:cmd(?:\.exe)?|(?:ch|mk|rm)?dir|[cmr]d|'
                        + br'del|erase|format|mo[vr]e|openfiles|path|'
                        + br'pushd|replace|robocopy|set|task(?:list|kill)|'
                        + br'tree|type|ipconfig|arp|awk|cat|cp|grep|head|'
                        + br'kill|find|locate|ln|ls|mv|nc|net(?:stat)?|'
                        + br'ps|pwd|rm|tail|touch)'
                        + br'[ \w\'\"*!.:/<>|\-\\]*[\"\'])\W',
                        re.IGNORECASE
                    ),
                },
                SuspiciousType.ENCRYPT: {
                    re.compile(br'\W((?:standard_|urlsafe_)?[ab](?:16|32|64|85)(?:hex)?(?:en|de)code)\s*\('),
                    re.compile(br'\W((?:strict_|urlsafe_)?(?:en|de)code64)\s*[({]'),
                    re.compile(br'\W(gzinflate)\s*\('),
                    re.compile(br'\W(base64_(?:en|de)code)\s*\('),
                    re.compile(br'\W(convert_uu(?:en|de)code)\s*\('),
                    re.compile(br'\W(str_rot13)\s*\('),
                    re.compile(br'\W(atob)\s*\('),
                    re.compile(br'\W(btoa)\s*\('),
                    re.compile(br'\W((?:From|To)Base64(?:Transform|String|CharArray))\W'),
                    re.compile(br'\W(SoapHexBinary)\W'),
                },
                SuspiciousType.FILES: {
                    re.compile(br'\W(FileStream)\W'),
                    re.compile(br'\W(FileMode\s*.\s*OpenOrCreate)\W'),
                    re.compile(br'\W(DriveInfo)\W'),
                    re.compile(br'\W(DirectoryInfo)\W'),
                    re.compile(br'\W(Create(?:Subd|D)irectory|SymbolicLink)\s*\('),
                    re.compile(br'\W(Enumerate(?:File(?:System(?:Infos)?|s)|Directories))\s*\('),
                    re.compile(
                        br'\W(Get(?:Drives|File(?:SystemEntries|s|Name|)|'
                        + br'(?:Current)?Directory(?:Name)?|Directories))\s*\('
                    ),
                    re.compile(br'\W(Open(?:Read|Text|Write))\s*\('),
                    re.compile(br'\W((?:Read|Write)All(?:Lines|Bytes|Text)(?:Async)?)\s*\('),
                    re.compile(br'\W(ReadLines(?:Async)?)\s*\('),
                    re.compile(br'\W((?:re|sys)open)\s*\('),
                    re.compile(br'\W(each_line)\s*[({]'),
                    re.compile(
                        br'\Wf(?:ile)?\s*\.\s*((?:write|read)(?:lines?)?)',
                        re.IGNORECASE
                    ),
                    re.compile(br'\W(directory\?)\s*\('),
                    re.compile(br'\W((?:read|execut)able(?:_real)?\?)\s*\('),
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
                    re.compile(br'\W(appendFile(?:Sync|))\s*\('),
                    re.compile(br'\W(create(?:Read|Write)Stream)\s*\('),
                    re.compile(br'\.(fd)\W'),
                    re.compile(br'\W(read(?:v|dir|[Ff]ile|link|[Ll]ines?|partial|ableWebStream)(?:Sync|))\s*\('),
                    re.compile(br'\W(write(?:v|File)(?:Sync|))\s*\('),
                    re.compile(br'\W(open(?:dir|AsBlob)(?:Sync|))\s*\('),
                    re.compile(br'\W(removedirs)\s*\('),
                    re.compile(
                        br'\W(eio_(?:f?ch(?:mod|own)|fallocate|'
                        + br'ftruncate|init|link|mk(?:dir|nod)|open|'
                        + br'read(?:dir|link)?|realpath|rmdir|'
                        + br'seek|sendfile|write))\s*\('
                    ),
                },
                SuspiciousType.IMPORT: {
                    re.compile(br'\W(include(?:_once)?\s*\(.+?\))'),
                    re.compile(br'\W(require\s*\(\s*[\"\'](?:fs|multer|express-fileupload|socket\.io)[\"\']\s*\))'),
                },
                SuspiciousType.NET: {
                    re.compile(br'\W(\$_FILES(?:\s*\[.+?])+)'),
                    re.compile(br'\W(Download(?:Data|File|String)(?:(?:Task)?Async)?)\s*\('),
                },
                SuspiciousType.OS: {
                    re.compile(br'\W(access)\s*\('),
                    re.compile(br'\.(environb?)\W'),
                    re.compile(br'\W(get(?:envb?|_exec_path))\s*\('),
                    re.compile(br'\W(putenv)\s*\('),
                },
            },
            DangerLevel.PAY_ATTENTION: {
                SuspiciousType.GENERAL: {
                    re.compile(br'\W([\"\']/bin/sh[\"\'])\W', re.IGNORECASE),
                    re.compile(br'((?:web)?shell(?:exec)?)', re.IGNORECASE),
                },
                SuspiciousType.EXECUTION: {
                    re.compile(br'\W(\$_GET\s*\[.+?])'),
                    re.compile(br'\W(\$_REQUEST\s*\[.+?])'),
                    re.compile(br'\W((?:popen|capture)(?:3|2e?))\s*\('),
                },
                SuspiciousType.FILES: {
                    re.compile(br'(with\s+open\(.+?\)\s+as.+?:)'),
                    re.compile(br'(=\s*open\(.+\))'),
                },
                SuspiciousType.IMPORT: {
                    re.compile(br'\W(require(?:_once)?\s*\(.+?\))'),
                },
                SuspiciousType.NET: {
                    re.compile(br'\W(urllib\.urlretrieve)\s*\('),
                    re.compile(br'\W(requests\.get)\s*\('),
                    re.compile(br'\W(Net\s*::\s*HTTP\s*\.\s*get(?:_response)?\s*\(.+\))'),
                    re.compile(br'\W(http\s*\.\s*request(?:_get)?\s*\(.+\))'),
                },
            },
        }

    def search(self, text: bytes) -> list[SuspiciousCode]:
        searched: set[SuspiciousCode] = set()
        for pc in self._get_next_pattern():
            found = set(pc.pattern.findall(text))
            for fnd in set(found):
                searched.add(SuspiciousCode(fnd, pc.danger_lvl, pc.type))
        return list(searched)

    def _get_next_pattern(self) -> Iterator[PatternContainer]:
        for lvl in self._patterns:
            for type_ in self._patterns[lvl]:
                for pat in self._patterns[lvl][type_]:
                    yield PatternContainer(pat, lvl, type_)


def main():
    # text = read_file('../../source/x.txt')
    text = input().encode()
    searched = SuspySearcher().search(text)
    for sr in searched:
        print(sr)


if __name__ == '__main__':
    main()
