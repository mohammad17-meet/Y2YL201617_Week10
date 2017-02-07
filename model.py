from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

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
    mvps = Column(Integer)
    myteam = relationship("Myteam", back_populates="player")


class Myteam(Base): 
    __tablename__ = 'myteam' 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    championships = Column(Integer)
    MVPs = Column(Integer)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("Player", back_populates="myteam" )



if __name__ == "__main__":
    engine = create_engine('sqlite:///project.db')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()