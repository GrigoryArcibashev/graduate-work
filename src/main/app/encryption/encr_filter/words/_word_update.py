from src.main.app.encryption.extractors.token_extractor import TokenExtractor, TokenType, Token
from src.main.app.encryption.extractors.word_extractor import WordExtractor
from src.main.app.file_reader import read_file


def read_as_text(path: str) -> set[str]:
    with open(path, 'r') as f:
        return set(map(lambda w: w.strip(), f.read().split()))


def map_bytes_to_str(byte_arr) -> str:
    return ''.join(map(chr, byte_arr))


def get_word_stream(token_extr, word_extr):
    prefixes = ['../../../../source/orig/']
    postfix = '.txt'
    files = [str(i) for i in range(8, 9)]
    for prefix in prefixes:
        for filename in files:
            print(f'\n---ФАЙЛ №{filename}---\n')
            text = list(read_file(prefix + filename + postfix))  # список из номеров
            yield from get_next_word(text, token_extr, word_extr)


def get_next_word(byte_text, token_extr, word_extr):
    for token in token_extr.get_token_iter(byte_text):
        if token.type == TokenType.LETTERS:
            for word in word_extr.get_word_iter(token.value):
                yield word


def main():
    token_extr = TokenExtractor()
    word_extr = WordExtractor()
    existed = read_as_text('words.txt')
    result = sorted(list(get_new_words(existed, token_extr, word_extr)))
    write_as_text(result)


def write_as_text(text_list):
    with open('words2.txt', mode='w', encoding='utf-8') as f:
        for line in text_list:
            f.write(f'{line}\n')


def get_new_words(words: set[str], token_extr, word_extr) -> set[str]:
    bad_words = set()
    for word_as_bytes in get_word_stream(token_extr, word_extr):
        word = map_bytes_to_str(word_as_bytes).lower()
        if word in words or word in bad_words or len(word) < 2:
            continue
        print(f'{repr(word)} | ', end='')
        # inp = False
        inp = input().strip().lower()
        if not inp:
            words.add(word)
        else:
            bad_words.add(word)
    return words


if __name__ == '__main__':
    main()
