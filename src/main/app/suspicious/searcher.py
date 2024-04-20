import re
from enum import Enum


class DangerLevel(Enum):
    DANGEROUS = 0
    SUSPICIOUS = 1
    PAY_ATTENTION = 2


class Language(Enum):
    PHP = 0,
    JS = 1
    PYTHON = 2
    RUBY = 3
    C_SHARP = 4


PATTERNS = {
    Language.PHP: {
        DangerLevel.DANGEROUS: (
            re.compile(br'eval\s*\('),
            re.compile(br'include(?:_once)?\s*\('),
            re.compile(br'require(?:_once)?\s*\('),

            re.compile(br'exec\s*\('),
            re.compile(br'passthru\s*\('),
            re.compile(br'proc_open\s*\('),
            re.compile(br'shell_exec\s*\('),
            re.compile(br'system\s*\('),

            re.compile(br'pcntl_exec\s*\('),
        ),
        DangerLevel.SUSPICIOUS: (
            re.compile(br'gzinflate\s*\('),
            re.compile(br'base64_(?:en|de)code\s*\('),
            re.compile(br'convert_uu(?:en|de)code\s*\('),
            re.compile(br'str_rot13\s*\('),

            re.compile(br'basename\s*\('),
            re.compile(br'ch(?:grp|mod|own)\s*\('),
            re.compile(br'clearstatcache\s*\('),
            re.compile(br'copy\s*\('),
            re.compile(br'dirname\s*\('),
            re.compile(br'disk(?:free|_free_|_total_)space\s*\('),
            re.compile(
                br'file(?:_exists|_get_contents|_put_contents|atime|'
                + br'ctime|group|inode|mtime|owner|perms|size|type)?\s*\('
            ),
            re.compile(
                br'f(?:close|eof|flush|get(?:csv|c|ss|s)|lock|nmatch|'
                + br'open|passthru|put(?:csv|s)|read|scanf|seek|stat|'
                + br'sync|tell|truncate|write)\s*\('),
            re.compile(br'glob\s*\('),
            re.compile(br'is_(?:dir|executable|file|link|readable|uploaded_file|write?able)\s*\('),
            re.compile(br'lch(?:grp|own)\s*\('),
            re.compile(br'link(?:info)?\s*\('),
            re.compile(br'lstat\s*\('),
            re.compile(br'mkdir\s*\('),
            re.compile(br'move_uploaded_file\s*\('),
            re.compile(br'parse_ini_(?:file|string)\s*\('),
            re.compile(br'pathinfo\s*\('),
            re.compile(br'pclose\s*\('),
            re.compile(br'popen\s*\('),
            re.compile(br'read(?:file|link)\s*\('),
            re.compile(br'realpath(?:_cache_(?:get|size))?\s*\('),
            re.compile(br're(?:name|wind)\s*\('),
            re.compile(br'rmdir\s*\('),
            re.compile(br'set_file_buffer\s*\('),
            re.compile(br'stat\s*\('),
            re.compile(br'symlink\s*\('),
            re.compile(br'tempnam\s*\('),
            re.compile(br'tmpfile\s*\('),
            re.compile(br'touch\s*\('),
            re.compile(br'umask\s*\('),
            re.compile(br'unlink\s*\('),

            re.compile(
                br'eio_(?:chmod|chown|fallocate|fchmod|fchown|'
                + br'fstat|fstatvfs|ftruncate|futime|init|link|'
                + br'lstat|mkdir|mknod|open|read|readdir|readlink|'
                + br'realpath|rename|rmdir|seek|sendfile|stat|statvfs|'
                + br'symlink|sync_file_range|truncate|unlink|utime|write)'
                + br'\s*\('
            )
        ),
        DangerLevel.PAY_ATTENTION: (
            re.compile(br'\$_GET\s*\['),
            re.compile(br'\$_POST\s*\['),
            re.compile(br'\$_REQUEST\s*\['),
        )
    }
}
