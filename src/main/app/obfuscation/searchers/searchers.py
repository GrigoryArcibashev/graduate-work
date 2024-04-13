import re
from typing import Iterator

from src.main.app.encryption.extractors.token_extractor import TokenExtractor, Token, TokenType
from src.main.app.obfuscation.searchers.common import Searcher, Language, Name


class VariableSearcher(Searcher):
    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = {
            Language.JS: [
                re.compile(rb'(?:let|var|const)\s+(\w+)((?:\s*,\s*\w+)*)\s*[=;]'),
                re.compile(rb'(?:let|var|const)\s+(\w+)((?:\s*=\s*\w+)*)\s*[=;]')
            ],
            Language.PYTHON_RUBY: [
                re.compile(rb'(\w+)((?: *, *\w+)*) *='),
                re.compile(rb'(\w+)((?: *= *\w+)*) *=')
            ],
            Language.PHP: [re.compile(rb'\$(\w+)\s*[=;]')]
        }

    def get_name_iter(self, string) -> Iterator[Name]:
        for lang in self._patterns:
            for pattern in self._patterns[lang]:
                found = pattern.findall(string)
                if not found:
                    continue
                for match in found[0]:
                    if match:
                        for name in self._extract_names(match):
                            yield Name(value=name, lang=lang)


class FunctionSearcher(Searcher):
    def __init__(self, token_extractor: TokenExtractor):
        super().__init__(token_extractor)
        self._patterns = {
            Language.JS: [
                re.compile(rb'function\s+(\w+)\s*\(((\s*\w+\s*,?)*)\s*\)\s*{'),
                re.compile(rb'(const\s+(\w+)\s*=\s*)?(\(((\s*\w+\s*,?)*)\)|(\s*\w+\s*))\s*=>')
            ],
            Language.PYTHON_RUBY: [
                re.compile(rb'def +(\w+) *\(((?: *\w+ *,?)*) *\) *:')
            ],
            Language.PHP: [re.compile(rb'function\s+(\w+)\s*\(((?:\s*\$\w+\s*,?)*)\s*\)\s*{')]
        }

    def get_name_iter(self, string) -> Iterator[Name]:
        pass


def main():
    text = b'123'  # b"let var1, var2 ;"
    var_searcher = VariableSearcher(TokenExtractor())
    for var in var_searcher.get_name_iter(text):
        print(f'ПЕРЕМЕННАЯ ({var.lang})')
        for name in var.value:
            print(f'\t{name}')
        print()


if __name__ == '__main__':
    main()
