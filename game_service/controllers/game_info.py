from game_service.models.game import Game
from game_service.swagger_server.models.game_info import GameInfo
from game_service.swagger_server.models.game_info_players import GameInfoPlayers

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
