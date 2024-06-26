from src.main.app.model.analyzer.analysis_result import AnalysisResult
from src.main.app.model.db_service.models import ScanResult, EncrResult, SuspyResult
from src.main.app.model.db_service.result_of_file_analysis import ResultOfFileAnalysis
from src.main.app.model.db_service.rw_service import ResultFromDB
from src.main.app.model.encryption.encryption_determinator.encr_analyze_result import EncrAnalyzeResult
from src.main.app.model.encryption.encryption_determinator.encryption_determinants.enums import EncrVerdict
from src.main.app.model.hasher.hash_service import HashResult
from src.main.app.model.obfuscation.obfuscation_determinator import ObfuscationResult
from src.main.app.model.suspicious.suspicious_code import SuspiciousCode


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
            _hash=HashResult(scan_result.hash),
            status=scan_result.status
        )

    @staticmethod
    def convert_to_db_models(results: list[ResultOfFileAnalysis]) -> list[ScanResult]:
        return list(map(ConverterForDB.convert_to_db_model, results))

    @staticmethod
    def convert_to_db_model(result: ResultOfFileAnalysis) -> ScanResult:
        filename = result.filename
        _hash = result.hash.hash()
        status = result.status
        encr = result.an_result.encr_res
        obf = result.an_result.obf_res
        suspy = result.an_result.suspy_res

        scan_res = ScanResult(
            filename=filename,
            hash=_hash,
            status=status,
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
