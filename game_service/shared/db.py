import os

from flask import current_app
from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from game_service.constants import URLS

if os.environ.get('GAME_SERVICE_SETTINGS') == 'localconfig.cfg':
    env = 'local'
else:
    env = 'container'

engine = create_engine(URLS[env].rdbs)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property

@retry(wait_fixed=2000, stop_max_attempt_number=10)
def init_db():
    # import models
    from game_service.models.game import Game
    Base.metadata.create_all(bind=engine)
