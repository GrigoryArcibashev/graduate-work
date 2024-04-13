import re
from enum import Enum
from typing import Iterator

from src.main.app.encryption.extractors.token_extractor import TokenExtractor
from src.main.app.obfuscation.searchers.common import Searcher


class Language(Enum):
    PHP = 0
    JS = 1
    C_SHARP = 2
    PYTHON = 3
    RUBY = 4
    PYTHON_OR_RUBY = 5

    def __str__(self):
        return self.name


class VariableSearcher(Searcher):
    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = {
            Language.PHP: (
                re.compile(rb'((?:\$\w+\s*=\s*)+)'),
                re.compile(rb'\$(\w+)((?:\s*,\s*\$\w+)*)'),
            ),
            Language.JS: (
                re.compile(rb'(?:let|var|const)\s+(\w+)((?:\s*,\s*\w+)*)\s*[=;]'),
                re.compile(rb'(?:let|var|const)\s+((?:\w+\s*=\s*)+)]')
            ),
            Language.PYTHON_OR_RUBY: (
                re.compile(rb'(\w+)((?: *, *\w+)*) *='),
                re.compile(rb'((?:\w+ *= *)+)')
            ),
            Language.C_SHARP: (
                # protected static readonly List<int , int, Float<double>>[,,] var1
                re.compile(
                    rb'(?:(?:private\s+protected\s|protected\s+internal\s)' +
                    rb'|(?:public\s|private\s|protected\s|internal\s|file\s))' +
                    rb'\s*(?:const\s|(?:static\s)?\s*(?:readonly\s)?)?' +
                    rb'\s*\w+\s*<[\w\s,<>]+>\s*\s*(?:\[[\s,]*])*\s+(\w+)'
                ),
                # }   List < int, int, Float < double >> [,, ] var1, var2, var3
                re.compile(rb'[};]\s*\w+\s*(?:<[\w\s,<>]+>)*\s*(?:\[[\s,]*])*\s+(\w+)((?:\s*,\s*\w+)*)\s*[=;]')
            )
        }

    @property
    def patterns(self) -> Iterator[re.Pattern]:
        for lang in self._patterns:
            print(f'>{lang}')
            for pattern in self._patterns[lang]:
                yield pattern


class FunctionSearcher(Searcher):

    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = {
            Language.JS: (
                re.compile(rb'function\s+(\w+)\s*\(((\s*\w+\s*,?)*)\s*\)\s*{'),
                re.compile(rb'(const\s+(\w+)\s*=\s*)?(\(((\s*\w+\s*,?)*)\)|(\s*\w+\s*))\s*=>')
            ),
            Language.PYTHON_OR_RUBY: (
                re.compile(rb'def +(\w+) *\(((?: *\w+ *,?)*) *\) *:')
            ),
            Language.PHP: (re.compile(rb'function\s+(\w+)\s*\(((?:\s*\$\w+\s*,?)*)\s*\)\s*{'))
        }

    @property
    def patterns(self) -> Iterator[re.Pattern]:
        for lang in self._patterns:
            for pattern in self._patterns[lang]:
                yield pattern


def main():
    variables = set()
    # text = b"let var1 = var2 = 12;"
    text = b"const var0 = 'string';\nlet var1 , var2 = 12, 22;"
    var_searcher = VariableSearcher(TokenExtractor())
    for var in var_searcher.get_name_iter(text):
        print('ПЕРЕМЕННАЯ', end='')
        print('_OLD' if var in variables else '_NEW')
        for name in var.value:
            print(f'\t{name}')
        print()
        variables.add(var)


if __name__ == '__main__':
    main()
