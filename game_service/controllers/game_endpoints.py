import json

import connexion
from flask import current_app, Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.shared.db import session, init_db


def create_new_game():
    """
    Endpoint for creating new game
    """
    players = request.get_json()
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

def get_game_info(gameId):
    """
    retrieve data for existing game
    """

    game = session.query(Game).filter(Game.id == gameId).first()
    return json.dumps({"game_id":game.id, "game_state":game.game_state, "players":game.players})
