import pickle

from numpy import mean, median

from src.main.app.extractors.word import Word
from src.main.app.file_reader import read_file


def read_as_text(path: str) -> set[str]:
    with open(path, 'r') as f:
        return set(map(lambda w: w.strip(), f.read().split()))


def read_as_bytes(path):
    return list(map(lambda x: tuple(x.strip()), read_file(path).split()))


def sort_and_stat_words(ws, path):
    lens = list(map(len, ws))
    print(f'MEAN = {round(mean(lens), 1)}\nMEDIAN = {median(lens)}')
    words = dict()
    for word in ws:
        length = len(word)
        if length not in words:
            words[length] = set()
        words[length].add(word)
    with open(path, 'w') as file:
        for word_len in sorted(words.keys()):
            print(f'{word_len}: {len(words[word_len])}')
            for word in sorted(words[word_len]):
                file.write(f'{word}\n')
    print()


def make_and_write_words_by_len(words, path_destin):
    result = dict()
    for word in words:
        length = len(word)
        if length not in result:
            result[length] = set()
        result[length].add(Word(word))
    with open(path_destin, 'wb') as f:
        pickle.dump(result, f)


if __name__ == '__main__':
    sort_and_stat_words(read_as_text('words.txt'), 'words.txt')
    make_and_write_words_by_len(read_as_bytes('words.txt'), 'words_by_len.bin')
