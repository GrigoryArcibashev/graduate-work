from sqlalchemy.orm import Session

from src.main.app.analyzer.analysis_result import AnalysisResult
from src.main.app.db_service.models import ScanResult, EncrResult, SuspyResult


class ResultPair:
    def __init__(self, filename: str, an_result: AnalysisResult):
        self._filename = filename
        self._an_result = an_result

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def an_result(self) -> AnalysisResult:
        return self._an_result


class Converter:
    @staticmethod
    def convert_to_db_models(result_pair: ResultPair) -> ScanResult:
        filename = result_pair.filename
        encr = result_pair.an_result.encr_res
        obf = result_pair.an_result.obf_res
        suspy = result_pair.an_result.suspy_res

        scan_res = ScanResult(
            filename=filename,
            encr=encr.is_encr,
            obf=obf.is_obf,
            suspy=bool(suspy)
        )
        encr_res = EncrResult(
            id=scan_res.id,
            filename=filename,
            entropy=encr.entr_verdict.is_encr,
            hex=encr.hex_verdict.is_encr
        )
        suspy_res = [
            SuspyResult(
                scan_id=scan_res.id,
                filename=filename,
                danger_lvl=suspicious_code.danger_lvl,
                suspy_type=suspicious_code.type,
                suspicious=suspicious_code.code_as_str
            )
            for suspicious_code in suspy
        ]
        scan_res.encr_result = [encr_res]
        scan_res.suspy_result = suspy_res

        return scan_res
