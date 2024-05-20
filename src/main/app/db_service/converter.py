from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main.app.analyzer.analysis_result import AnalysisResult
from src.main.app.db_service.models import ScanResult, EncrResult, SuspyResult, Base
from src.main.app.encryption.encryption_determinator.encr_analyze_result import EncrAnalyzeResult
from src.main.app.encryption.encryption_determinator.encryption_determinants.enums import EncrVerdict
from src.main.app.hasher.hash_service import HashResult, Hasher
from src.main.app.obfuscation.obfuscation_determinator import ObfuscationResult
from src.main.app.settings.hash_settings import HashSettings
from src.main.app.suspicious.enums import SuspiciousType, DangerLevel
from src.main.app.suspicious.suspicious_code import SuspiciousCode


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
    def convert_from_db_models(scan_result: ScanResult) -> ResultOfFileAnalysis:
        encr_result: EncrResult = scan_result.encr_result[0]
        suspy_result: list[SuspyResult] = scan_result.suspy_result

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
    def convert_to_db_models(result: ResultOfFileAnalysis) -> ScanResult:
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


def delete_main(engine, session):
    with session(autoflush=False, bind=engine) as db:
        for sc_r in db.query(ScanResult).all():
            db.delete(sc_r)
        db.commit()


def create_main(engine, session):
    with session(autoflush=False, bind=engine) as db:
        sc_r1 = create_record_to_db('file_1')
        sc_r2 = create_record_to_db('file_2')
        sc_r3 = create_record_to_db('file_3')
        db.add_all([sc_r1, sc_r2, sc_r3])
        db.commit()


def get_main(engine, session):
    with session(autoflush=False, bind=engine) as db:
        return list(map(ConverterForDB.convert_from_db_models, list(db.query(ScanResult).all())))


def main():
    sqlite_database = "sqlite:///../../database.db"
    engine = create_engine(sqlite_database)
    # создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("База данных и таблица созданы")

    session = sessionmaker(autoflush=False, bind=engine)

    delete_main(engine, session)
    create_main(engine, session)
    for res in get_main(engine, session):
        print(res)


def create_record_to_db(filename: str) -> ScanResult:
    hasher = Hasher(HashSettings({'algs': {'sha256': 'sha256'}, 'alg': 'sha256'}))
    result_of_file_analysis = ResultOfFileAnalysis(
        filename=filename,
        an_result=AnalysisResult(
            encr_res=EncrAnalyzeResult(
                hex_verdict=EncrVerdict.NOT_DETECTED,
                entr_verdict=EncrVerdict.DETECTED
            ),
            obf_res=ObfuscationResult(
                is_obf=True
            ),
            suspy_res=[
                SuspiciousCode(
                    code=f'code_{filename}'.encode(),
                    danger_lvl=DangerLevel.DANGEROUS,
                    suspy_type=SuspiciousType.FILES
                ),
                SuspiciousCode(
                    code=f'code_{filename}'.encode(),
                    danger_lvl=DangerLevel.SUSPICIOUS,
                    suspy_type=SuspiciousType.NET
                )
            ]
        ),
        old_hash=hasher.calc_hash(f'old_hash_{filename}'.encode()),
        new_hash=hasher.calc_hash(f'new_hash_{filename}'.encode()),
    )

    return ConverterForDB.convert_to_db_models(result_of_file_analysis)


if __name__ == '__main__':
    main()
