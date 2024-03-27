from src.main.app.encryption.extractors.token_extractor import TokenExtractor, TokenType, Token
from src.main.app.encryption.extractors.word_extractor import WordExtractor
from src.main.app.file_reader import read_file


def read_as_text(path: str) -> set[str]:
    with open(path, 'r') as f:
        return set(map(lambda w: w.strip(), f.read().split()))


def write_as_text(text_list, filename):
    with open(filename, mode='w', encoding='cp1251') as f:
        for line in text_list:
            f.write(f'{line}\n')


def map_bytes_to_str(byte_arr) -> str:
    return ''.join(map(chr, byte_arr))


def get_next_word(byte_text, token_extr, word_extr):
    for token in token_extr.get_token_iter(byte_text):
        if token.type == TokenType.LETTERS:
            for word in word_extr.get_word_iter(token.value):
                yield word


def get_word_stream(token_extr, word_extr):
    # filename = '../../../../source/encr/12.txt'
    filename = 'words2.txt'
    text = list(read_file(filename))  # список из номеров
    yield from get_next_word(text, token_extr, word_extr)


def get_new_words(words: set[str], token_extr, word_extr) -> set[str]:
    bad_words = set()
    for word_as_bytes in get_word_stream(token_extr, word_extr):
        word = map_bytes_to_str(word_as_bytes).lower()
        if word in words or word in bad_words or len(word) < 3:
            continue
        # print(f'{repr(word)} | ', end='')
        inp = False
        # inp = input().strip().lower()
        if not inp:
            words.add(word)
        else:
            bad_words.add(word)
    return words


def main():
    token_extr = TokenExtractor()
    word_extr = WordExtractor()
    existed = read_as_text('words.txt')
    result = sorted(list(get_new_words(existed, token_extr, word_extr)))
    write_as_text(result, 'words.txt')


def filter_english(text: list[str]):
    rus_letters = set('йцукенгшщзхъфывапролджэячсмитьбюё' + 'йцукенгшщзхъфывапролджэячсмитьбюё'.upper())
    result = []
    for symb in text:
        if symb in rus_letters:
            continue
        result.append(symb)
    return ''.join(result)


def remove_rus_letters(src: str, tgt: str):
    with open(src, 'r', encoding='utf-8') as f:
        result = filter_english(list(f.read())).lower()

    with open(tgt, 'w', encoding='utf-8') as f:
        f.write(result)


if __name__ == '__main__':
    remove_rus_letters('./raw_words.txt', './words2.txt')
    # main()
