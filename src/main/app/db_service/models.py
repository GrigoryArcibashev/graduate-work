from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship, Session


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
    danger_lvl = Column(String, nullable=False)
    suspy_type = Column(String, nullable=False)
    suspicious = Column(String, nullable=False)

    scan_result = relationship('ScanResult', back_populates='suspy_result')


def main():
    # engine = create_engine("sqlite:///../../database.db")

    sqlite_database = "sqlite:///metanit.db"
    engine = create_engine(sqlite_database)
    # создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("База данных и таблица созданы")

    with Session(autoflush=False, bind=engine) as db:
        # sc_r1 = ScanResult(filename='file_1', encr=True, obf=True, suspy=True)
        # en_r1 = EncrResult(filename='file_1', entropy=True, hex=True)
        # su_r1 = SuspyResult(scan_id=1, filename='file_1', danger_lvl='DANGER', suspy_type='SUSPY', suspicious='CODE')
        # sc_r1.encr_result = [en_r1]
        # sc_r1.suspy_result = [su_r1]
        # db.add(sc_r1)
        #
        # sc_r2 = ScanResult(filename='file_2', encr=False, obf=False, suspy=False)
        # en_r2 = EncrResult(filename='file_2', entropy=False, hex=False)
        # su_r2 = SuspyResult(scan_id=2, filename='file_1', danger_lvl='DANGER', suspy_type='SUSPY', suspicious='CODE')
        # sc_r2.encr_result = [en_r2]
        # sc_r2.suspy_result = [su_r2]
        # db.add(sc_r2)

        for sc_r in db.query(ScanResult).all():
            db.delete(sc_r)

        db.commit()


if __name__ == '__main__':
    main()
