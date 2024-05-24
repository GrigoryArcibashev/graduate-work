from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main.app.db_service.models import ScanResult, Base, EncrResult, SuspyResult


class ResultFromDB:
    def __init__(self, scan_result: ScanResult, encr_result: list[EncrResult], suspy_result: list[SuspyResult]):
        self.scan_result = scan_result
        self.encr_result = encr_result
        self.suspy_result = suspy_result


class DBService:
    def __init__(self, path_to_db: str):
        self._engine = create_engine(path_to_db)  # "sqlite:///../../database.db"
        Base.metadata.create_all(bind=self._engine)

    def read(self) -> list[ResultFromDB]:
        session = sessionmaker(autoflush=False, bind=self._engine)
        with session(autoflush=False, bind=self._engine) as db:
            sc_results: list[ScanResult] = db.query(ScanResult).all()
            return [ResultFromDB(sc_r, sc_r.encr_result, sc_r.suspy_result) for sc_r in sc_results]

    def write(self, scan_results: list[ScanResult]) -> None:
        session = sessionmaker(autoflush=False, bind=self._engine)
        self._delete(session)
        self._write(session, scan_results)

    def _delete(self, session) -> None:
        with session(autoflush=False, bind=self._engine) as db:
            for sc_r in db.query(ScanResult).all():
                db.delete(sc_r)
            db.commit()

    def _write(self, session, scan_results: list[ScanResult]):
        with session(autoflush=False, bind=self._engine) as db:
            db.add_all(scan_results)
            db.commit()


def main():
    service = DBService('sqlite:///../../database.db')
    for sc_r in service.read():
        print(sc_r.suspy_result)


if __name__ == '__main__':
    main()
