import json

from game_service.shared.oas_clients import player_service_client

def register_pending_player(account_id=None, game_id=None):
    """
    make request to player service to register a new pending player
    """
    results, request_status = player_service_client.newPlayer.create_new_player(
        newPlayerRequest={
            'accountId': account_id,
            'gameId': game_id
        }
    ).result()

    return results.player_id

def activate_pending_player(player_id=None, starting_phase=None):
    """
    send request to player service to activate pending player
    """
    result, status = player_service_client.gameOperations.activate_player(
        activatePlayerRequest={
            'playerId': player_id,
            'startingPhase': starting_phase
        }
    ).result()

def player_phase_change(player_id=None, requested_phase=None):
    """
    sends request to player service to change player phase
    """
    result, query_status = player_service_client.gameOperations.player_phase_change(
        phaseChangeRequest= {
            'playerId': player_id,
            'requestedPhase': requested_phase
        }
    ).result()
