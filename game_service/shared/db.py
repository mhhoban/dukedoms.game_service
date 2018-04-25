import os

from flask import current_app
from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from game_service.constants import URLS

if os.environ.get('GAME_SERVICE_ENV') == 'local':
    env = 'local'
else:
    env = 'container'

engine = create_engine(URLS[env].rdbs)
Base = declarative_base()

def get_new_db_session():
    return scoped_session(sessionmaker(bind=engine))

@retry(wait_fixed=2000, stop_max_attempt_number=10)
def init_db():
    # import models
    from game_service.models.game import Game

    session = get_new_db_session()
    try:
        Base.query = session.query_property
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()
