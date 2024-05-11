from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class ScanResult(Base):
    __tablename__ = 'scan_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False, unique=True)
    encr = Column(Boolean)
    obf = Column(Boolean)
    suspy = Column(Boolean)

    encr_result = relationship('EncrResult', back_populates='scan_result')
    suspy_result = relationship('SuspyResult', back_populates='scan_result')


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

    # строка подключения
    sqlite_database = "sqlite:///metanit.db"

    # создаем движок SqlAlchemy
    engine = create_engine(sqlite_database)

    # создаем таблицы
    Base.metadata.create_all(bind=engine)

    print("База данных и таблица созданы")


if __name__ == '__main__':
    main()
