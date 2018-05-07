import json

from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.models.game_proxy import GameProxy
from game_service.models.game_state import GameState
from game_service.models.game_state_proxy import GameStateProxy
from game_service.shared.db import get_new_db_session
from game_service.shared.oas_clients import account_service_client, player_service_client
from game_service.shared.player_service_calls import player_phase_change
from game_service.swagger_server.models.game_info import GameInfo
from game_service.swagger_server.models.game_info_players import GameInfoPlayers


def end_player_turn():
    """
    Endpoint to end a player's turn and start the turn of the next player in the game's turn order
    """
    game_id = request.get_json()['gameId']
    player = request.get_json()['playerEmail']

    game = GameProxy(game_id)
    game_state = GameStateProxy(game_id)

    #get ID for player ending turn
    ending_player_id = game.get_player_id(player)

    #get ID for next player in line
    next_player_email = game_state.get_next_player_email(current_player=player)
    next_player_id = game.get_player_id(next_player_email)

    # End current player turn
    player_phase_change(player_id=ending_player_id, requested_phase='inactive')
    # Start next player turn
    player_phase_change(player_id=next_player_id, requested_phase='action')

    game_state.update_active_player_id(next_player_id)

    return None, status.HTTP_200_OK
