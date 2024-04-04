# Description: This file contains the model classes for the database.
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

class Cal(Base):
    __tablename__ = 'cal'

    id = mapped_column(Integer, primary_key=True)
    rdow = mapped_column(Integer)
    rdom = mapped_column(Integer)
    edate = mapped_column(String)
    etime = mapped_column(String)
    etext = mapped_column(String)

    def __repr__(self):
        return (f'<Cal(rdow={self.rdow}, edate={self.edate}, etime={self.etime}, etext={self.etext})>')
