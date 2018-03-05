import json

from flask import Flask, request
from flask.ext.api import status
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
        return json.dumps({'game_created': False, 'reason': 'missing players'}), status.HTTP_400_BAD_REQUEST

    game_state = 'pending'
    new_game = Game(game_state=game_state, players=players)
    session.add(new_game)

    try:
        session.commit()
        response = {'game_created': True, 'game_id': new_game.id}

    except SQLAlchemyError:
        response = {'game_created': False}

    response = json.dumps(response)
    return response, status.HTTP_200_OK

@app.route('/getGame/<int:game_id>', methods=['GET'])
def get_game_info(game_id):
    """
    retrieve data for existing game
    """

    game = session.query(Game).filter(Game.id == game_id).first()
    return json.dumps({"game_id":game.id, "game_state":game.game_state, "players":game.players})
