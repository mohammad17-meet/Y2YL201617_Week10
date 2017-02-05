from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
class Person(Base):
	__tablename__ = 'person' 
	id = Column(Integer, primary_key=True)
	name = Column(String)  
	email = Column(String)
	password = Column(String)
class Player(Base): 
	__tablename__ = 'player' 
	id = Column(Integer, primary_key=True)
	name = Column(String)
	champs = Column(Integer)
	MVPs = Column(Integer)
	myteam = relationship("Myteam", back_populates="myteam")


class Myteam(Base): 
	__tablename__ = 'myteam' 
	id = Column(Integer, primary_key=True)
	name = Column(String)
	championships = Column(Integer)
	MVPs = Column(Integer)
	player_id = Column(Integer, ForeignKey('player.id'))
	players = relationship("Player", back_populates=("myteam")
