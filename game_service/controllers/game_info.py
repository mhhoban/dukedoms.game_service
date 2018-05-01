import json

from flask_api import status

from game_service.models.game import Game
from game_service.shared.db import get_new_db_session
from game_service.swagger_server.models.game_info import GameInfo
from game_service.swagger_server.models.game_info_players import GameInfoPlayers

def get_game_info(gameId):
    """
    retrieve data for existing game
    """

    session = get_new_db_session()
    game = session.query(Game).filter(Game.id == gameId).first()

    game_players = GameInfoPlayers(
        host_player=game.host_player,
        invited_players=json.loads(game.invited_players),
        accepted_players=json.loads(game.accepted_players),
        declined_players=json.loads(game.declined_players),
        pending_players=json.loads(game.pending_players)
    )

    game_info = GameInfo(
        game_id=game.id,
        players=game_players
    )

    session.close()

    return game_info.to_dict(), status.HTTP_200_OK
