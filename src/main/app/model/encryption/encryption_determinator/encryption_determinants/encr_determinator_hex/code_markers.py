MARKERS = (
    (br'\xef', br'\xbb', br'\xbf'),  # UTF8
    (br'0xef', br'0xbb', br'0xbf'),
    (br'\xff', br'\xfe'),  # UTF16 LE
    (br'0xff', br'0xfe'),
    (br'\xfe', br'\xff'),  # UTF16 BE
    (br'0xfe', br'0xff'),
    (br'\xff', br'\xfe', br'\x00', br'\x00'),  # UTF32 LE
    (br'0xff', br'0xfe', br'0x00', br'0x00'),
    (br'\x00', br'\x00', br'\xfe', br'\xff'),  # UTF32 BE
    (br'0x00', br'0x00', br'0xfe', br'0xff'),
    (br'\x2b', br'\x2f', br'\x76', br'\x38'),  # UTF7 (1)
    (br'0x2b', br'0x2f', br'0x76', br'0x38'),
    (br'\x2b', br'\x2f', br'\x76', br'\x39'),  # UTF7 (2)
    (br'0x2b', br'0x2f', br'0x76', br'0x39'),
    (br'\x2b', br'\x2f', br'\x76', br'\x2b'),  # UTF7 (3)
    (br'0x2b', br'0x2f', br'0x76', br'0x2b'),
    (br'\x2b', br'\x2f', br'\x76', br'\x2f'),  # UTF7 (4)
    (br'0x2b', br'0x2f', br'0x76', br'0x2f'),
    (br'\xf7', br'\x64', br'\x4c'),  # UTF1
    (br'0xf7', br'0x64', br'0x4c'),
    (br'\xdd', br'\x73', br'\x66', br'\x73'),  # UTF-EBCDIC
    (br'0xdd', br'0x73', br'0x66', br'0x73'),
)
