from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main.app.db_service.models import ScanResult, Base


class DBService:
    def __init__(self, path_to_db: str):
        self._engine = create_engine(path_to_db)  # "sqlite:///../../database.db"
        Base.metadata.create_all(bind=self._engine)

    def read(self) -> list[ScanResult]:
        session = sessionmaker(autoflush=False, bind=self._engine)
        with session(autoflush=False, bind=self._engine) as db:
            return list(db.query(ScanResult).all())

    def update(self, scan_results: list[ScanResult]) -> None:
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
