from typing import Optional

from src.main.app.model.analyzer.analysis_result import AnalysisResult
from src.main.app.model.db_service.models import ScanResult, EncrResult, SuspyResult
from src.main.app.model.db_service.rw_service import ResultFromDB
from src.main.app.model.encryption.encryption_determinator.encr_analyze_result import EncrAnalyzeResult
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import EncrVerdict
from src.main.app.model.hasher.hash_service import HashResult
from src.main.app.model.obfuscation.obfuscation_determinator import ObfuscationResult
from src.main.app.model.suspicious.suspicious_code import SuspiciousCode


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

    def __str__(self):
        return f'{self.filename}\nold_h: {self.old_hash}\nnew_h: {self.new_hash}\n{self.an_result}'


class ConverterForDB:
    @staticmethod
    def convert_from_db_models(scan_results: list[ResultFromDB]) -> list[ResultOfFileAnalysis]:
        return list(map(ConverterForDB.convert_from_db_model, scan_results))

    @staticmethod
    def convert_from_db_model(result_from_db: ResultFromDB) -> ResultOfFileAnalysis:
        scan_result: ScanResult = result_from_db.scan_result
        encr_result: EncrResult = result_from_db.encr_result[0]
        suspy_result: list[SuspyResult] = result_from_db.suspy_result

        an_result = AnalysisResult(
            encr_res=EncrAnalyzeResult(
                hex_verdict=EncrVerdict.DETECTED if encr_result.hex else EncrVerdict.NOT_DETECTED,
                entr_verdict=EncrVerdict.DETECTED if encr_result.entropy else EncrVerdict.NOT_DETECTED
            ),
            obf_res=ObfuscationResult(
                is_obf=scan_result.obf
            ),
            suspy_res=[
                SuspiciousCode(
                    code=sus_res.suspicious,
                    danger_lvl=sus_res.danger_lvl,
                    suspy_type=sus_res.suspy_type
                )
                for sus_res in suspy_result
            ]
        )

        return ResultOfFileAnalysis(
            filename=scan_result.filename,
            an_result=an_result,
            old_hash=HashResult(scan_result.old_hash) if scan_result.old_hash else None,
            new_hash=HashResult(scan_result.new_hash) if scan_result.new_hash else None,
        )

    @staticmethod
    def convert_to_db_models(results: list[ResultOfFileAnalysis]) -> list[ScanResult]:
        return list(map(ConverterForDB.convert_to_db_model, results))

    @staticmethod
    def convert_to_db_model(result: ResultOfFileAnalysis) -> ScanResult:
        filename = result.filename
        old_hash = result.old_hash.hash() if result.old_hash else None
        new_hash = result.new_hash.hash() if result.new_hash else None
        encr = result.an_result.encr_res
        obf = result.an_result.obf_res
        suspy = result.an_result.suspy_res

        scan_res = ScanResult(
            filename=filename,
            old_hash=old_hash,
            new_hash=new_hash,
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
