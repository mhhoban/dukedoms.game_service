from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://dukedoms:daleria@localhost:5432/game_service')
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property

def init_db():
    # import models
    from game_service.models.game import Game
    Base.metadata.create_all(bind=engine)
