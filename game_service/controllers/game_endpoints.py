import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.shared.db import session
from game_service.swagger_server.models.new_game_success_response import NewGameSuccessResponse
from game_service.swagger_server.models.new_game_failed_response import NewGameFailedResponse
from game_service.swagger_server.models.game_info import GameInfo
from game_service.swagger_server.models.game_info_players import GameInfoPlayers


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
        response = NewGameSuccessResponse(
            game_created=True,
            game_id=new_game.id
        )

    except SQLAlchemyError:
        response = NewGameFailedResponse(
            game_created=False
        )

    return response.to_dict(), status.HTTP_200_OK

def get_game_info(gameId):
    """
    retrieve data for existing game
    """

    game = session.query(Game).filter(Game.id == gameId).first()

    game_players = GameInfoPlayers(
        host_player=game.host_player,
        invited_players=game.invited_players
    )

    game_info = GameInfo(
        game_id=game.id,
        players=game_players
    )

    return game_info.to_dict(), status.HTTP_200_OK
