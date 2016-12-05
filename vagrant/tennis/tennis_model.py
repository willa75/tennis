import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Player(Base):
    __tablename__ = 'player'
    name = Column(
        String(80), nullable = False)
    id = Column(
        Integer, primary_key = True)

class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key = True)
    points = Column(Integer, nullable= False)
    player_id = Column(
        Integer, ForeignKey('player.id'), unique=True)
    player = relationship(Player)

engine = create_engine('sqlite:///tennis.db')

Base.metadata.create_all(engine)