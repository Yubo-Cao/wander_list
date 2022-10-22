import datetime
import enum
from typing import *

from sqlalchemy import Column, Integer, String, DateTime, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Category(enum.Enum):
    CULTURE = 1
    FOOD = 2
    OUTDOORS = 3
    SHOPPING = 4
    SPORTS = 5
    LANDMARK = 6


class Event(Base):
    __tablename__ = "events"

    name: str = Column(String(100), primary_key=True)
    description: str = Column(String(500))
    location: str = Column(String(200))
    date: datetime.date = Column(DateTime)
    ranking: int = Column(Integer)
    category: Category = Column(Enum(Category))


class Level(enum.Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    WORLD_TRAVELER = 4


Timeline = List[Event]


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(20), unique=True)
    password: str = Column(String(20))
    email: str = Column(String(50))
    level: Level = Column(Enum(Level))
    timeline: Timeline = relationship("Event", back_populates="user")


class Thread(Base):
    __tablename__ = "threads"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(100))
    user: User = relationship("User", back_populates="thread")
    create_time: datetime = Column(DateTime)
    content: str = Column(String(500))


# sqlite
engine = create_engine("sqlite:///travel.db", echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
