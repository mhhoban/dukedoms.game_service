import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.shared.db import session, init_db
from game_service.config import GameServiceConfig

app = connexion.App(__name__, specification_dir='swagger/')
app.app.config.from_object(GameServiceConfig)
app.app.config.from_envvar('GAME_SERVICE_SETTINGS')

app.add_api('game_service_api.yaml')
@retry(wait_fixed=2000, stop_max_number_attempts=10)
init_db()
app.run(port=5000)
