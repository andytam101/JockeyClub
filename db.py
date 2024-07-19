from sqlalchemy import create_engine, Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///data.db"


Base = declarative_base()


class Horse(Base):
    __tablename__ = "horse"

    id = Column(String, primary_key=True)
    name = Column(String)


class Race(Base):
    __tablename__ = "race"

    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    distance = Column(Integer)
    highQuality = Column(Boolean, default=False)
    fair = Column(Enum("fair", "quick", "catch"), default="fair")  # quick = 快放，catch = 後上
    url = Column(String)


class Ran(Base):
    __tablename__ = "ran"

    raceId = Column(Integer, primary_key=True)
    horseId = Column(String, primary_key=True)
    ranking = Column(Integer)


def get_session():
    session = sessionmaker(bind=_engine)
    return session()


_engine = create_engine(DB_PATH)
Base.metadata.create_all(_engine)
