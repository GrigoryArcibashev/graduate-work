import pickle

from _word_update import read_as_text
from numpy import mean, median

from src.main.app.extractors.word import Word
from src.main.app.file_reader import read_file


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


def write_from_func(words_before, words_after):
    sort_and_stat_words(words_before, 'words2.txt')
    sort_and_stat_words(words_after, 'raw_words.txt')


def func():
    words_before = read_as_text('words.txt')
    words_after = set()  # words_before.copy()
    words_n_m = filter(lambda w: len(w) == 12, words_before.copy())
    for word in words_n_m:
        print(f'\tСЛОВО - {word}')
        if input():
            continue

        word_orig = word
        print(f'WORD = {word_orig}')
        word_len_before = word_len_prev = len(word_orig)
        true = True
        while true:
            if word[:3] in ('get', 'set'):
                word = word[3:]
            if word[:2] == 'ip':
                word = word[2:]

            for pref_ind in range(len(word), 1, -1):
                if pref_ind == word_len_before:
                    continue
                if word[:pref_ind] in words_before:
                    print(f'Найдено:  {word[:pref_ind]}')
                    word = word[pref_ind:]
                    break
            if len(word) == word_len_prev:
                true = False
            else:
                word_len_prev = len(word)
        print(f'!Остаток:  {word}')
        if len(word) != word_len_before:
            print(f'>Оригинальное слово удалено')
            words_before.discard(word_orig)
            if len(word) > 3 and word not in words_before:
                print('>ОСТАТОК ЗАПИСАН')
                words_after.add(word)
        print()
    write_from_func(words_before, words_after)


def make_and_write_words_by_len(words, path_destin):
    result = dict()
    for word in words:
        length = len(word)
        if length not in result:
            result[length] = set()
        result[length].add(Word(word))
    with open(path_destin, 'wb') as f:
        pickle.dump(result, f)


def read_as_bytes(path):
    return list(map(lambda x: tuple(x.strip()), read_file(path).split()))


if __name__ == '__main__':
    sort_and_stat_words(read_as_text('words.txt'), 'words.txt')
    make_and_write_words_by_len(read_as_bytes('words.txt'), 'words_by_len.bin')