import re
from abc import abstractmethod
from re import Pattern
from typing import Iterator

from src.main.app.extractors.token import Token, TokenType
from src.main.app.extractors.token_extractor import TokenExtractor
from src.main.app.file_reader import read_file
from src.main.app.obfuscation.searchers.name import Name


class AbstractSearcher:
    def __init__(self, token_extractor: TokenExtractor):
        self._token_extractor = token_extractor

    @property
    @abstractmethod
    def patterns(self) -> tuple[Pattern]:
        pass

    def get_name_iter(self, text: bytes) -> Iterator[Name]:
        names = set()
        for pattern in self.patterns:
            found = pattern.findall(text)
            if not found:
                continue
            for group_num in range(len(found)):
                for match in self._wrap_in_tuple_if_necessary(found[group_num]):
                    if not match:
                        continue
                    for name in self._extract_names(match):
                        if name not in names:
                            names.add(name)
                            yield Name(value=name)

    @staticmethod
    def _wrap_in_tuple_if_necessary(group):
        if not isinstance(group, tuple):
            return (group,)
        return group

    def _extract_names(self, raw_str) -> Iterator[tuple[Token]]:
        current_name = list()
        for token in self._token_extractor.get_token_iter(list(raw_str)):
            if self._is_token_include_in_name(token, current_name):
                current_name.append(token)
            elif self._is_name_over(token, current_name):
                yield tuple(current_name)
                current_name.clear()
        if current_name:
            yield tuple(current_name)

    @staticmethod
    def _is_token_include_in_name(token: Token, current_name: list[Token]):
        return (
                token.type == TokenType.LETTERS
                or token.type == TokenType.UNDERLINING
                or current_name and token.type == TokenType.DIGITS
        )

    @staticmethod
    def _is_name_over(token: Token, current_name: list[Token]):
        return current_name and token.type != TokenType.UNDERLINING


class VariableSearcher(AbstractSearcher):
    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = (
            # PHP
            re.compile(rb'((?:\$\w+\s*=\s*)+)'),
            re.compile(rb'\$(\w+)((?:\s*,\s*\$\w+)*)'),
            re.compile(rb'(?:array\s*\(|\[)\s*\"(\w+)\"\s*=>'),

            # PYTHON, RUBY, JS and C#
            re.compile(rb'(\w+)((?:\s*,\s*\w+)*)\s*(?:=[^=]|;)'),
            re.compile(rb'((?:\w+\s*=[^=]+?)+)'),

            # C#
            # }   List < int, int, Float < double >> [,, ] var1, var2, var3
            re.compile(rb'\w+\s*(?:<[.,<>\w\s]*>)?\s*(?:\[[\s,]*])*\s+(\w+)((?:\s*,\s*\w+)*)\s*[=;{]')
        )

    @property
    def patterns(self) -> Iterator[re.Pattern]:
        for pattern in self._patterns:
            print(f'\n{"-" * len(str(pattern))}\n{pattern}\n{"-" * len(str(pattern))}')
            yield pattern


class FunctionSearcher(AbstractSearcher):
    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = (
            # JS
            # function func(var1, var2, var3){ ИЛИ function (var1, var2, var3){
            re.compile(rb'function(?:\s+(\w+)|)\s*\(((?:\s*\w+\s*,?)*)\s*\)\s*{'),
            # Функциональный стиль и lambda
            re.compile(rb'(?:const\s+(\w+)\s*=\s*)?(?:\(.*?\)|\s*\w+\s*)\s*=>'),

            # PYTHON and RUBY
            # def func(var1, *args1, ** args2)
            re.compile(rb'def +(\w+) *\(((?: *\*{,2} *\w+ *(?:,|=.*?)?)*) *\)'),

            # PYTHON
            re.compile(rb'(\w+) *= *lambda[ \w,]+:'),

            # RUBY
            # my_lambda = -> (v) { puts "hello "+v }
            re.compile(rb'(\w+) *= *-> *(?:\([ \w,]*\))? *(?:{|do)'),
            # my_lambda = lambda { puts "hello" }
            re.compile(rb'(\w+) *= *lambda *(?:{|do)'),

            # PHP
            # function displayInfo($name, ...$age){
            re.compile(rb'function\s+(\w+)\s*\(((?:\s*(?:\.\.\.)?\$\w+\s*(?:,|=.*?)?)*)\s*\)\s*{'),
            # $displayInfo = function($name, $age){
            re.compile(rb'\$(\w+)\s*=\s*function\s*\(((?:\s*(?:\.\.\.)?\$\w+\s*(?:,|=.*?)?)*)\s*\)\s*{'),

            # C_SHARP
            re.compile(
                rb'\w+\s*(?:<[.,<>\w\s]*>)?\s*(?:\[[\s,]*])*\s+(\w+)\s*(?:<[.,<>\w\s]*>)?\s*\(.*?\)\s*(?:{|=>|;)'
            )
        )

    @property
    def patterns(self) -> Iterator[re.Pattern]:
        for pattern in self._patterns:
            print(f'\n{"-" * len(str(pattern))}\n{pattern}\n{"-" * len(str(pattern))}')
            yield pattern


class ClassSearcher(AbstractSearcher):
    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = (
            # RUBY
            re.compile(rb'class +(\w+) *(?:< *(\.\w+) *)?[\n;#]'),

            # C#
            re.compile(rb'(?:class|interface)\s+(\w+)\s*(?:<[.,<>\w\s]*>)?(?:\s*(?:where .*?)?\s*:.*?)?\s*{'),

            # PYTHON
            re.compile(rb'class +(\w+) *(?:\(.*?\))? *:'),

            # PHP and JS (уже есть C#; тут то, что не найдет в C#)
            re.compile(rb'(?:class|trait)\s+(\w+)(?:\s+extends .*?)?\s*{')
        )

    @property
    def patterns(self) -> Iterator[re.Pattern]:
        for pattern in self._patterns:
            print(f'\n{"-" * len(str(pattern))}\n{pattern}\n{"-" * len(str(pattern))}')
            yield pattern


def main():
    variables = set()
    text = read_file('../../../source/x.txt')
    var_searcher = ClassSearcher(TokenExtractor())
    for var in var_searcher.get_name_iter(text):
        print('OLD' if var in variables else 'NEW', end=' VARIABLE\n')
        for name in var.value:
            print(f'\t{name}')
        print()
        variables.add(var)
    print(f'Кол-во уникальных имён: {len(variables)}')


if __name__ == '__main__':
    main()
