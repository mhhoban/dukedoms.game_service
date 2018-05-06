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
