import json

from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.models.game_proxy import GameProxy
from game_service.models.game_state import GameState
from game_service.shared.db import get_new_db_session
from game_service.shared.oas_clients import account_service_client, player_service_client
from game_service.shared.account_service_calls import new_hosted_game, send_invite
from game_service.shared.player_service_calls import activate_pending_player
from game_service.swagger_server.models.new_game_success_response import NewGameSuccessResponse


def create_new_game():
    """
    Endpoint for creating new game
    """
    players = request.get_json()
    new_game_id = create_new_game_entry(players)
    invited_players = players['invitedPlayers']

    game = GameProxy(new_game_id)
    # Add host player:
    game.add_accepted_player(account_id=players['hostPlayerId'], player_email=players['hostPlayer'])
    host_player_game_id = game.get_player_id(players['hostPlayer'])

    new_hosted_game(player_id=host_player_game_id, account_id=players['hostPlayerId'])

    send_invite(game_id=new_game_id, players=invited_players)
    response = NewGameSuccessResponse(
        game_created=True,
        game_id=new_game_id
    )
    return response.to_dict(), status.HTTP_200_OK


def accept_invite():
    acceptance_info = request.get_json()
    game_id = acceptance_info['gameId']
    player_email = acceptance_info['playerEmail']
    account_id = acceptance_info['accountId']

    game = GameProxy(game_id)
    game.player_accepts_invite(player_email=player_email, account_id=account_id, game_id=game_id)

    # Check for remaining pending players
    if game.start_game_check():
        start_game(game_id)

    return {'gameId': game_id, 'playerId': game.get_player_id(player_email)}, status.HTTP_200_OK


def start_game(game_id):
    """
    Handles initial work of getting game state ready for play
    """

    game = GameProxy(game_id)
    turn_order = [player for player in game.get_accepted_players()]

    player_one_id = game.get_player_id(turn_order[0])
    player_one_email = turn_order[0]

    session = get_new_db_session()
    game_state = GameState(game_id=game_id, player_turn_order=turn_order, active_player_id=player_one_id)
    session.add(game_state)
    session.commit()
    session.close()

    for player in turn_order:
        phase = 'action' if player == player_one_email  else 'inactive'
        player_id = game.get_player_id(player)
        activate_pending_player(player_id=player_id, starting_phase=phase)


def decline_invite():
    decline_info = request.get_json()
    game_id = decline_info['gameId']
    player_email = decline_info['playerEmail']

    game = GameProxy(game_id)

    game.player_declines_invite(decline_info['playerEmail'])


########################
# Helpers

def create_new_game_entry(players):
    """
    perform SQLAlchemy Footwork of creating new game entry
    """
    host_player = players['hostPlayer']
    host_player_id = players['hostPlayerId']
    invited_players = players['invitedPlayers']
    game_state = 'pending'
    new_game = Game(
        game_state=game_state,
        invited_players=invited_players,
        host_player=host_player
    )
    session = get_new_db_session()
    session.add(new_game)
    session.commit()
    new_game_id = new_game.id
    session.close()
    return new_game_id
