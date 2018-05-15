import json

from flask_api import status

from game_service.models.game import Game
from game_service.models.game_proxy import GameProxy

from game_service.shared.db import get_new_db_session
from game_service.swagger_server.models.game_info import GameInfo
from game_service.swagger_server.models.game_info_players import GameInfoPlayers

def get_player_id(gameId, playerEmail):

    game = GameProxy(gameId)
    player_email = playerEmail
    return {'playerId': game.get_player_id(player_email)}, status.HTTP_200_OK

def get_game_info(gameId):
    """
    retrieve data for existing game
    """
    game_id = gameId
    game = GameProxy(game_id)
    return game.get_game_info(), status.HTTP_200_OK
