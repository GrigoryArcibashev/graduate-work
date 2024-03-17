from typing import Iterator


class ExtractorInterface:
    def next_element(self, string) -> Iterator:
        """
        Returns the next selected element (defined by the implementation) from the string
        :param string: sequence of bytes (b'...' or iterable[bytes])
        """
        pass
