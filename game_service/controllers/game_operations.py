import json

import connexion
from flask import Flask, request
from flask_api import status
from sqlalchemy.exc import SQLAlchemyError

from game_service.models.game import Game
from game_service.models.game_state import GameState
from game_service.shared.db import get_new_db_session
from game_service.shared.oas_clients import account_service_client, player_service_client
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
    host_player_id = players['hostPlayerId']
    invited_players = players['invitedPlayers']['invitedPlayers']
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

    # Add host player:
    result, result_status = player_service_client.newPlayer.create_new_player(
        newPlayerRequest= {
            'accountId': host_player_id,
            'gameId': new_game.id
        }
    ).result()
    host_player_game_id = result.player_id
    result, result_status = account_service_client.gameOperations.new_hosted_game(
        newHostedGameRequest= {
            'playerId': host_player_game_id,
            'accountId': host_player_id
        }
    ).result()

    session = get_new_db_session()
    game = session.query(Game).filter(Game.id == new_game_id).first()

    game.accepted_players = json.loads(game.accepted_players)
    game.accepted_players['acceptedPlayers'].append(host_player)
    accepted_players = json.dumps(game.accepted_players)
    session.query(Game).filter(Game.id == new_game_id).update(
        {"accepted_players":accepted_players}
    )
    session.commit()

    game.player_ids = json.loads(game.player_ids)
    game.player_ids['playerIds'][host_player] = host_player_game_id
    player_ids = json.dumps(game.player_ids)
    session.query(Game).filter(Game.id == new_game_id).update(
        {"player_ids":player_ids}
    )
    session.commit()

    session.close()

    send_invite(game_id=new_game.id, players=invited_players)
    response = NewGameSuccessResponse(
        game_created=True,
        game_id=new_game_id
    )
    return response.to_dict(), status.HTTP_200_OK

def send_invite(game_id=None, players=None):
    """
    send invite to account service
    """
    result, status = account_service_client.gameOperations.invite_accounts(
        invitationBatch= {
            'gameId': game_id,
            'playerList': players
        }
    ).result()


def accept_invite():
    acceptance_info = request.get_json()
    game_id = acceptance_info['gameId']
    player_email = acceptance_info['playerEmail']
    account_id = acceptance_info['accountId']

    session = get_new_db_session()
    game = session.query(Game).filter(Game.id == game_id).first()

    # TODO Not Sloppy JSON entry editing
    game.accepted_players = json.loads(game.accepted_players)
    game.pending_players = json.loads(game.pending_players)
    game.player_ids = json.loads(game.player_ids)

    if not verify_player_pending(
        submitted_player=player_email,
        pending_players=game.pending_players['pendingPlayers']
    ):
        return status.HTTP_400_BAD_REQUEST

    player_accept_invite(
        accepted_player=player_email,
        pending_players=game.pending_players['pendingPlayers']
    )

    try:

        # hit new player endpoint
        result, result_status = player_service_client.newPlayer.create_new_player(
            newPlayerRequest = {
                'accountId': account_id,
                'gameId': game_id
            }
        ).result()

        game.accepted_players['acceptedPlayers'].append(player_email)

        game.player_ids['playerIds'][player_email] = result.player_id
        # game.player_ids['playerIds'].append({player_email:result.player_id})

        accepted_players = json.dumps(game.accepted_players)
        pending_players = json.dumps(game.pending_players)
        player_ids = json.dumps(game.player_ids)

        session.query(Game).filter(Game.id == game_id).update(
            {"accepted_players":accepted_players}
        )
        session.query(Game).filter(Game.id == game_id).update(
            {"pending_players":pending_players}
        )
        session.query(Game).filter(Game.id == game_id).update(
            {"player_ids":player_ids}
        )
        session.commit()

        return {'gameId': result.game_id, 'playerId': result.player_id}, status.HTTP_200_OK
    except SQLAlchemyError:
        raise SQLAlchemyError
    finally:
        pending_players = len(json.loads(game.pending_players)['pendingPlayers'])
        session.close()

        # Check for remaining pending players
        if  pending_players < 1:
            start_game(game_id)


def start_game(game_id):
    """
    Handles initial work of getting game state ready for play
    """
    session = get_new_db_session()
    game = session.query(Game).filter(Game.id == game_id).first()
    player_ids = json.loads(game.player_ids)['playerIds']

    #Construct Player Turn List
    turn_order = [player for player in json.loads(game.accepted_players)['acceptedPlayers']]

    player_one_id = player_ids[turn_order[0]]
    player_one_email = turn_order[0]

    game_state = GameState(game_id=game_id, player_turn_order=turn_order, active_player_id=player_one_id)
    session.add(game_state)
    session.commit()
    session.close()

    for player in turn_order:
        phase = 'Action' if player == player_one_email  else 'Inactive'
        player_id = player_ids[player]
        result, status = player_service_client.gameOperations.activate_player(
            activatePlayerRequest={
                'playerId': player_id,
                'startingPhase': phase
            }
        ).result()


def decline_invite():
    decline_info = request.get_json()
    game_id = decline_info['gameId']
    player_email = decline_info['playerEmail']

    session = get_new_db_session()
    game = session.query(Game).filter(Game.id == game_id).first()
    # TODO Not Sloppy JSON entry editing
    game.declined_players = json.loads(game.declined_players)
    game.pending_players = json.loads(game.pending_players)

    if not verify_player_pending(
        submitted_player=player_email,
        pending_players=game.pending_players['pendingPlayers']
    ):
        return status.HTTP_400_BAD_REQUEST

    player_decline_invite(
        declined_player=player_email,
        declined_players=game.declined_players['declinedPlayers'],
        pending_players=game.pending_players['pendingPlayers']
    )

    session = get_new_db_session()
    try:
        declined_players = json.dumps(game.declined_players)
        pending_players = json.dumps(game.pending_players)

        session.query(Game).filter(Game.id == game_id).update(
            {"declined_players":declined_players}
        )
        session.query(Game).filter(Game.id == game_id).update(
            {"pending_players":pending_players}
        )
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

def player_accept_invite(accepted_player=None, pending_players=None):

    if verify_player_pending(submitted_player=accepted_player, pending_players=pending_players):
        pending_players.remove(accepted_player)
        return True

    else:
        return False
