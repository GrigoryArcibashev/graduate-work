def write_test_words(words: list[str], path: str) -> None:
    with open(path, 'w') as f:
        for word in words:
            f.write(f'{word}\n')


def map_str_to_numbers(string: str) -> tuple[int]:
    return tuple(map(ord, string))
