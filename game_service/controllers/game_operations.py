import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.shared.db import get_new_db_session
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
    session = get_new_db_session()

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
    finally:
        session.close()

    return response.to_dict(), status.HTTP_200_OK


def accept_invite():
    acceptance_info = request.get_json()
    game_id = acceptance_info['gameId']
    player_email = acceptance_info['playerEmail']

    game = session.query(Game).filter(Game.id == game_id).first()

    if not verify_player_pending(
        submitted_player=player_email,
        pending_players=game.pending_players
    ):
        return status.HTTP_400_BAD_REQUEST

    player_accept_invite(
        accepted_player=player_email,
        accepted_players=game.accepted_players,
        pending_players=game.pending_players
    )

    session = get_new_db_session()
    try:
        session.commit()
        return {'gameId': 13, 'playerId': 1337}, status.HTTP_200_OK
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()


def decline_invite():
    decline_info = request.get_json()
    game_id = decline_info['gameId']
    player_email = decline_info['playerEmail']

    game = session.query(Game).filter(Game.id == game_id).first()

    if not verify_player_pending(
        submitted_player=player_email,
        pending_players=game.pending_players
    ):
        return status.HTTP_400_BAD_REQUEST

    player_decline_invite(
        declined_player=player_email,
        declined_players=game.declined_players,
        pending_players=game.pending_players
    )

    session = get_new_db_session()
    try:
        session.commit()
        status.HTTP_200_OK
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        session.close()


def verify_player_pending(submitted_player=None, pending_players=None):
    """
    Verify a given player is still pending before proceeding with accept/decline
    """

    try:
        pending_players.index(submitted_player)
        return True
    except ValueError:
        return False


def player_decline_invite(declined_player=None, declined_players=None, pending_players=None):
    if verify_player_pending(submitted_player=declined_player, pending_players=pending_players):
        pending_players.remove(declined_player)
        declined_players.append(declined_player)
        return True

    else:
        return False

def player_accept_invite(accepted_player=None, accepted_players=None, pending_players=None):
    if verify_player_pending(submitted_player=accepted_player, pending_players=pending_players):
        pending_players.remove(accepted_player)
        accepted_players.append(accepted_player)
        return True

    else:
        return False
