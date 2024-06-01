from enum import Enum
from typing import Optional

from src.main.app.model.analyzer.analysis_result import AnalysisResult
from src.main.app.model.hasher.hash_service import HashResult


class Status(Enum):
    UNTRUSTED_NEW = 0
    UNTRUSTED_MODIFIED = 1
    TRUSTED = 2


class ResultOfFileAnalysis:
    def __init__(
            self,
            filename: str,
            an_result: AnalysisResult,
            old_hash: Optional[HashResult],
            new_hash: Optional[HashResult]
    ):
        self._filename = filename
        self._an_result = an_result
        self._old_hash = old_hash
        self._new_hash = new_hash

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def an_result(self) -> AnalysisResult:
        return self._an_result

    @property
    def old_hash(self) -> Optional[HashResult]:
        return self._old_hash

    @property
    def new_hash(self) -> Optional[HashResult]:
        return self._new_hash

    @property
    def status(self) -> Status:
        if self.old_hash is None:
            if self.new_hash is None:
                raise Exception('old and new hashes are None')
            return Status.UNTRUSTED_NEW
        if self.new_hash is None:
            return Status.TRUSTED
        return Status.UNTRUSTED_MODIFIED

    def __str__(self):
        return f'{self.filename}\nold_h: {self.old_hash}\nnew_h: {self.new_hash}\n{self.an_result}'

