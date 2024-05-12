from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine, Enum
from sqlalchemy.orm import DeclarativeBase, relationship, Session, sessionmaker

from src.main.app.suspicious.enums import SuspiciousType, DangerLevel


class Base(DeclarativeBase):
    pass


class ScanResult(Base):
    __tablename__ = 'scan_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False, unique=True)
    encr = Column(Boolean)
    obf = Column(Boolean)
    suspy = Column(Boolean)

    encr_result = relationship('EncrResult', back_populates='scan_result', cascade='all, delete-orphan')
    suspy_result = relationship('SuspyResult', back_populates='scan_result', cascade='all, delete-orphan')


class EncrResult(Base):
    __tablename__ = 'encr_results'
    id = Column(Integer, ForeignKey('scan_results.id'), primary_key=True, unique=True)
    filename = Column(String, nullable=False, unique=True)
    entropy = Column(Boolean)
    hex = Column(Boolean)

    scan_result = relationship('ScanResult', back_populates='encr_result')


class SuspyResult(Base):
    __tablename__ = 'suspy_results'
    id = Column(Integer, primary_key=True, unique=True)
    scan_id = Column(Integer, ForeignKey('scan_results.id'))
    filename = Column(String, nullable=False)
    danger_lvl = Column(Enum(DangerLevel), nullable=False)
    suspy_type = Column(Enum(SuspiciousType), nullable=False)
    suspicious = Column(String, nullable=False)

    scan_result = relationship('ScanResult', back_populates='suspy_result')


def main():
    # engine = create_engine("sqlite:///../../database.db")

    sqlite_database = "sqlite:///metanit.db"
    engine = create_engine(sqlite_database)
    # создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("База данных и таблица созданы")

    session = sessionmaker(autoflush=False, bind=engine)

    with session(autoflush=False, bind=engine) as db:
        sc_r1 = method_name('file_1')
        sc_r2 = method_name('file_2')
        sc_r3 = method_name('file_3')

        db.add_all([sc_r1, sc_r2, sc_r3])
        db.commit()

    # with session(autoflush=False, bind=engine) as db:
    #     for sc_r in db.query(ScanResult).all():
    #         db.delete(sc_r)
    #     db.commit()


def method_name(filename: str):
    sc_r1 = ScanResult(filename=filename, encr=True, obf=True, suspy=True)
    en_r1 = EncrResult(id=sc_r1.id, filename=filename, entropy=True, hex=True)
    su_r1 = SuspyResult(scan_id=sc_r1.id, filename=filename, danger_lvl=DangerLevel.DANGEROUS,
                        suspy_type=SuspiciousType.FILES, suspicious=f'code {filename}')
    sc_r1.encr_result = [en_r1]
    sc_r1.suspy_result = [su_r1]
    return sc_r1


if __name__ == '__main__':
    main()
