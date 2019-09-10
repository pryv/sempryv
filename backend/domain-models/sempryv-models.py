from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float, Boolean, JSON, Index, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///orfeas-example.db')
Base = declarative_base()


class TestTable(Base):
    __tablename__ = 'test_table'
    stop_word = Column(String(100), primary_key=True)
    language = Column(String(50))
    model = Column(BLOB)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    touched_by = Column(String(100))


Base.metadata.create_all(bind=engine)
session = scoped_session(sessionmaker(bind=engine))
