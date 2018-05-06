import json

from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.models.game_state import GameState
from game_service.shared.db import get_new_db_session
from game_service.shared.oas_clients import account_service_client, player_service_client
from game_service.swagger_server.models.game_info import GameInfo
from game_service.swagger_server.models.game_info_players import GameInfoPlayers


def end_player_turn():
    """
    Endpoint to end a player's turn and start the turn of the next player in the game's turn order
    """
    game_id = request.get_json()['gameId']
    player = request.get_json()['playerEmail']

    session = get_new_db_session()
    game = session.query(Game).filter(Game.id == game_id).first()
    game_state = session.query(GameState).filter(GameState.game_id == game_id).first()

    #get ID for player ending turn
    ending_player_id = json.loads(game.player_ids)['playerIds'][player]

    #get ID for next player in line
    starting_player_index = (json.loads(game_state.player_turn_order)['player_turn_order'].index(player)) + 1
    starting_player_email = json.loads(game_state.player_turn_order)['player_turn_order'][starting_player_index]
    starting_player_id = json.loads(game.player_ids)['playerIds'][starting_player_email]

    # End current player turn
    result, query_status = player_service_client.gameOperations.player_phase_change(
        phaseChangeRequest= {
            'playerId': ending_player_id,
            'requestedPhase': 'inactive'
        }
    ).result()

    # Start next player turn
    result, query_status = player_service_client.gameOperations.player_phase_change(
        phaseChangeRequest= {
            'playerId': starting_player_id,
            'requestedPhase': 'action'
        }
    ).result()

    session.query(GameState).filter(GameState.game_id == game_id).update(
        {'active_player_id': starting_player_id}
    )
    session.commit()
    session.close()
    return None, status.HTTP_200_OK
