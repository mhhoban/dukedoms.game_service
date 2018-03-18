import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.shared.db import session


def create_new_game():
    """
    Endpoint for creating new game
    """
    players = request.get_json()
    host_player = players['hostPlayer']
    invited_players = players['invitedPlayers']
    game_state = 'pending'
    new_game = Game(
        game_state=game_state,
        invited_players=invited_players,
        host_player=host_player
    )
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
    return json.dumps(
        {
            "gameId":game.id,
            "gameState":game.game_state,
            "hostPlayer":game.host_player,
            "invitedPlayers":game.invited_players,
            "acceptedPlayers":game.accepted_players,
            "pendingPlayers":game.pending_players,
            "declinedPlayers":game.declined_players
        }
    )
