from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from model import *
engine = create_engine('sqlite:///project.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

Kareem_abd_aljabbar =Player(name="kareem abdul jabbar", champs="6", mvps="6")
micheal_jordon  =Player(name="michael jordan", champs="6", mvps="5")
bill_russel =Player(name="bill russel", champs="11", mvps="-")
magic_johnson =Player(name="magic johnson", champs="5", mvps="5")
wilt_chamberlain =Player(name="wilt chamberlain", champs="2", mvps="4")
kobe_bryant =Player(name="kobe bryant", champs="5", mvps="1")
tim_duncan =Player(name="tim duncan", champs="5", mvps="2")
shaquille_oneal =Player(name="shaq", champs="4", mvps="1")
larry_bird =Player(name="larry bird", champs="3", mvps="3")

session.add(Kareem_abd_aljabbar)
session.add(micheal_jordon)
session.add(magic_johnson)
session.add(bill_russel)
session.add(shaquille_oneal)
session.add(tim_duncan)
session.add(larry_bird)
session.add(kobe_bryant)
session.add(wilt_chamberlain)

session.commit()