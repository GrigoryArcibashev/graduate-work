import re
from typing import Iterator

from src.main.app.suspicious.enums import DangerLevel, SuspiciousType
from src.main.app.suspicious.suspicious_code import SuspiciousCode
from src.main.app.util.file_reader import read_file


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
                    re.compile(br'(?:[^\w\'\"]|^)([Ee]val)(?:\s+[\'\"\w]|\s*\()'),
                    re.compile(br'(?:[^\w\'\"]|^)(passthru)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(proc_open)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(system)(?:\s+[\'\"\w]|\s*\()'),
                    re.compile(
                        br'(?:[^\w\'\"]|^)((?:shell_|pcntl_)?exec(?:File|[vl]p?e?|)(?:Sync|))(?:\s+[\'\"\w]|\s*\()'
                    ),
                    re.compile(br'(?:[^\w\'\"]|^)(ICodeCompiler)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(CodeDom\.Compiler[.;])\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(CodeAnalysis\.(?:CSharp\.)?Scripting[.;])\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(CSharpScript\.(?:Run|Evaluate)Async)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(innerHTML)\s*\('),
                },
            },
            DangerLevel.SUSPICIOUS: {
                SuspiciousType.COMMAND: {
                    re.compile(
                        br'([\"\']\s*'
                        + br'(?:(?:ch|mk|rm)?dir|[cmr]d|openfiles|'
                        + br'pushd|robocopy|ipconfig|arp|awk|cp|grep|locate|ln|ls|'
                        + br'mv|nc|netstat|ps|pwd|rm|touch)'
                        + br'(?:\s+(?:--?[\s\w\'\"*!.:/<>|\-\\]*)*)?[\"\'])',
                        re.IGNORECASE
                    ),
                },
                SuspiciousType.ENCRYPT: {
                    re.compile(br'[_\W](rot_?(?:1[38]|47))', re.IGNORECASE),
                    re.compile(
                        br'[_\W]((?:ascii|base|radix)_?'
                        + br'(?:16|3[26]|45|5[68]|6[24]|85|9[14]|12[25]|xml)'
                        + br'_?(?:hex|url)?)',
                        re.IGNORECASE
                    ),
                    re.compile(
                        br'(?:[^\w\'\"]|^)((?:standard_|urlsafe_)?[ab](?:16|32|64|85)(?:hex)?(?:en|de)code)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)((?:strict_|urlsafe_)?(?:en|de)code64)\s*[({]'),
                    re.compile(br'(?:[^\w\'\"]|^)(gzinflate)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(base64_(?:en|de)code)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(convert_uu(?:en|de)code)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(str_rot13)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(atob)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(btoa)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)((?:From|To)Base64(?:Transform|String|CharArray))\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(SoapHexBinary)\W'),
                },
                SuspiciousType.FILES: {
                    re.compile(br'(?:[^\w\'\"]|^)(FileStream)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(FileMode\s*.\s*OpenOrCreate)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(DriveInfo)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(DirectoryInfo)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(Create(?:(?:Subd|D)irectory|SymbolicLink))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(Enumerate(?:File(?:System(?:Infos)?|s)|Directories))\s*\('),
                    re.compile(
                        br'(?:[^\w\'\"]|^)(Get(?:Drives|File(?:SystemEntries|s|Name|)|'
                        + br'(?:Current)?Directory(?:Name)?|Directories))\s*\('
                    ),
                    re.compile(br'(?:[^\w\'\"]|^)(Open(?:Read|Text|Write))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)((?:Read|Write)(?:All)?(?:Lines|Bytes|Text)(?:Async)?)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)((?:re|sys)open)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(each_line)\s*[({]'),
                    re.compile(br'(?:[^\w\'\"]|^)(directory\?)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)((?:read|execut)able(?:_real)?\?)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)([lf]?ch(?:grp|mod|own)(?:Sync|))\s*\('),
                    re.compile(
                        br'(?:[^\w\'\"]|^)(file_?(?:read|write|exists|(?:ge|pu)t_contents|inode|size|type|\?))\s*\('),
                    re.compile(
                        br'(?:[^\w\'\"]|^)'
                        + br'(f(?:cntl|open|passthru|read|scanf|[lr]?seek|(?:data)?sync|stat|write))\s*\('
                    ),
                    re.compile(br'(?:[^\w\'\"]|^)(dirname)\s*\('),
                    re.compile(
                        br'(?:[^\w\'\"]|^)(is_?(?:dir|executable|file|link|readable|uploaded_file|write?able))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(mk(?:dirs?|node)(?:Sync|))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(move_uploaded_file)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(pathinfo)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(p(?:open|readv?|writev?|ipe))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(rm(?:dir|)(?:Sync|))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(appendFile(?:Sync|))\s*\('),
                    re.compile(br'\.(fd)\W'),
                    re.compile(
                        br'(?:[^\w\'\"]|^)'
                        + br'(read(?:v|dir|[Ff]iles?|links?|[Ll]ines?|partial|ableWebStream)'
                        + br'(?:Sync|))\s*\('
                    ),
                    re.compile(br'(?:[^\w\'\"]|^)(write(?:v|[Ff]iles?|[Ll]ines?|links?)(?:Sync|))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(open(?:dir|AsBlob)(?:Sync|))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(removedirs)\s*\('),
                    re.compile(
                        br'(?:[^\w\'\"]|^)(eio_(?:f?ch(?:mod|own)|fallocate|'
                        + br'ftruncate|init|link|mk(?:dir|nod)|open|'
                        + br'read(?:dir|link)?|realpath|rmdir|'
                        + br'seek|sendfile|write))\s*\('
                    ),
                },
                SuspiciousType.IMPORT: {
                    re.compile(
                        br'(?:[^\w\'\"]|^)(require\s*\(\s*[\"\'](?:fs|multer|express-fileupload|socket\.io)[\"\']\s*\))'),
                },
                SuspiciousType.NET: {
                    re.compile(br'(?:[^\w\'\"]|^)(\$_FILES(?:\s*\[.+?])+)'),
                    re.compile(br'(?:[^\w\'\"]|^)(Download(?:Data|File|String)(?:(?:Task)?Async)?)\s*\('),
                },
                SuspiciousType.OS: {
                    re.compile(br'(?:[^\w\'\"]|^)(access)\s*\('),
                    re.compile(br'\.(environb?)\W'),
                    re.compile(br'(?:[^\w\'\"]|^)(get(?:envb?|_exec_path))\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(putenv)\s*\('),
                },
            },
            DangerLevel.PAY_ATTENTION: {
                SuspiciousType.GENERAL: {
                    re.compile(br'(?:[^\w\'\"]|^)([\"\']cmd(?:\.exe)?[\"\'])\W', re.IGNORECASE),
                    re.compile(br'(?:[^\w\'\"]|^)([\"\']/bin/sh[\"\'])\W', re.IGNORECASE),
                    re.compile(br'((?:web)?shell(?:exec)?)', re.IGNORECASE),
                },
                SuspiciousType.EXECUTION: {
                    re.compile(br'(?:[^\w\'\"]|^)(\$_GET\s*\[.+?])'),
                    re.compile(br'(?:[^\w\'\"]|^)(\$_REQUEST\s*\[.+?])'),
                    re.compile(br'(?:[^\w\'\"]|^)((?:popen|capture)(?:3|2e?))\s*\('),
                },
                SuspiciousType.FILES: {
                    re.compile(br'(with\s+open\(.+?\)\s+as.+?:)'),
                    re.compile(br'(=\s*open\(.+\))'),
                },
                SuspiciousType.IMPORT: {
                    re.compile(br'(?:[^\w\'\"]|^)((?:include|require)(?:_once)?\s*\(.+?\))'),
                },
                SuspiciousType.NET: {
                    re.compile(br'(?:[^\w\'\"]|^)(urllib\.urlretrieve)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(requests\.get)\s*\('),
                    re.compile(br'(?:[^\w\'\"]|^)(Net\s*::\s*HTTP\s*\.\s*get(?:_response)?\s*\(.+\))'),
                    re.compile(br'(?:[^\w\'\"]|^)(http\s*\.\s*request(?:_get)?\s*\(.+\))'),
                },
            },
        }

    def search(self, text: bytes) -> list[SuspiciousCode]:
        searched: set[SuspiciousCode] = set()
        for pc in self._get_next_pattern():
            found = set(pc.pattern.findall(text))
            for fnd in found:
                searched.add(SuspiciousCode(fnd, pc.danger_lvl, pc.type))
        return list(searched)

    def _get_next_pattern(self) -> Iterator[PatternContainer]:
        for lvl in self._patterns:
            for type_ in self._patterns[lvl]:
                for pat in self._patterns[lvl][type_]:
                    yield PatternContainer(pat, lvl, type_)


def main():
    text = read_file('../../source/FOR_TEST_X/x.txt')
    # text = input().encode()
    searched = SuspySearcher().search(text)
    for sr in searched:
        print(sr)


if __name__ == '__main__':
    main()
