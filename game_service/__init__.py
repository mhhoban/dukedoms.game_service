import json

from flask import Flask, request
from sqlalchemy.exc import SQLAlchemyError

from game_service.data_validation.data_validators import validate_new_game_request
from game_service.models.game import Game
from game_service.shared.db import session, init_db

init_db()
app = Flask(__name__)

@app.route('/newGame', methods=['POST'])
def create_new_game():
    """
    Endpoint for creating new game
    """
    players = request.get_json()

    if not validate_new_game_request(players):
        return json.dumps({'game_created': False, 'reason': 'missing players'})

    game_state = 'pending'
    new_game = Game(game_state=game_state, players=players)
    session.add(new_game)

    try:
        session.commit()
        status = {'game_created': True, 'game_id': new_game.id}

    except SQLAlchemyError:
        status = {'game_created': False}

    status = json.dumps(status)
    return status
