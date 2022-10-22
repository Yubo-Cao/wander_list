import dataclasses
import datetime
from enum import Enum
from typing import *

form sqlalchemy import Column, Integer, String, DateTime, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Category(Enum):
    CULTURE = 1
    FOOD = 2
    OUTDOORS = 4
    SHOPPING = 5
    SPORTS = 6
    LANDMARK = 7

@dataclasses.dataclass
class Event(Base):
    __tablename__ = "events"

    name: str = Column(String(100), primary_key=True)
    description: str = Column(String(500))
    location: str = Column(String(200))
    date: datetime.date = Column(DateTime)
    ranking: int = Column(Integer)
    category: Category = Column(Enum(Category))


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    WORLD_TRAVELER = 4


Timeline = List[Event]


@dataclasses.dataclass
class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(20))
    password: str = Column(String(20))
    email: str = Column(String(50))
    level: Level = Column(Enum(Level))
    timeline: Timeline = relationship("Event", back_populates="user")


@dataclasses
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
