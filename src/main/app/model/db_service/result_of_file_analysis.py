from enum import Enum

from src.main.app.model.analyzer.analysis_result import AnalysisResult
from src.main.app.model.hasher.hash_service import HashResult


class FileModStatus(Enum):
    UNTRUSTED = 0
    MODIFIED = 1
    TRUSTED = 2

    def to_str(self) -> str:
        if self == FileModStatus.UNTRUSTED:
            return 'недоверенный'
        if self == FileModStatus.MODIFIED:
            return 'изменённый'
        if self == FileModStatus.TRUSTED:
            return 'доверенный'

    def __str__(self):
        return self.to_str()


class ResultOfFileAnalysis:
    def __init__(
            self,
            filename: str,
            an_result: AnalysisResult,
            _hash: HashResult,
            status: FileModStatus
    ):
        self._filename = filename
        self._an_result = an_result
        self._hash = _hash
        self._status = status

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def an_result(self) -> AnalysisResult:
        return self._an_result

    @property
    def hash(self) -> HashResult:
        return self._hash

    @property
    def status(self) -> FileModStatus:
        return self._status

    def __str__(self):
        return f'{self.filename}\nhash: {self.hash}\nstatus: {self.status}\n{self.an_result}'
