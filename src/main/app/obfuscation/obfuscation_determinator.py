from src.main.app.obfuscation.name_processor import NameInfo, NameProcessor


class ObfuscationChecker:
    def check(self, name_info: NameInfo) -> bool:
        """
        :return: True (obf) / False (no obf)
        """
        pass


class ObfuscationDeterminator:
    def __init__(self, name_processor: NameProcessor, obfuscation_checker: ObfuscationChecker):
        self._name_processor = name_processor
        self._obfuscation_checker = obfuscation_checker

    def determinate(self, text):
        count = obf_count = 0
        for name_info in self._name_processor.get_next_name_info(text):
            count += 1
            if self._obfuscation_checker.check(name_info):
                obf_count += 1
        # TODO переделать
        return round(100 * obf_count / count, 2)
