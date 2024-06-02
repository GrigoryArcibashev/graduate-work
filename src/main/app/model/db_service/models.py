from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, relationship

from src.main.app.model.db_service.result_of_file_analysis import FileModStatus
from src.main.app.model.suspicious.enums import SuspiciousType, DangerLevel


class Base(DeclarativeBase):
    pass


class ScanResult(Base):
    __tablename__ = 'scan_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False, unique=True)
    hash = Column(String)
    status = Column(Enum(FileModStatus), nullable=False)
    encr = Column(Boolean)
    obf = Column(Boolean)
    suspy = Column(Boolean)

    encr_result = relationship('EncrResult', back_populates='scan_result', cascade='all, delete-orphan')
    suspy_result = relationship('SuspyResult', back_populates='scan_result', cascade='all, delete-orphan')

    def __str__(self):
        result = f'id = {self.id}, ' \
                 f'filename = {self.filename}, ' \
                 f'hash(6) = {str(self.hash)[:6]}' \
                 f'status = {str(self.status)}'
        return result


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
