import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.data_validation.data_validators import validate_new_game_request
from game_service.models.game import Game
from game_service.shared.db import session, init_db

init_db()
app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('game_service_api.yaml')
app.run(port=5000)
