import json

from game_service.shared.oas_clients import account_service_client


def new_hosted_game(player_id=None, account_id=None):
    """
    make request to add game host created to account info
    """
    result, result_status = account_service_client.gameOperations.new_hosted_game(
        newHostedGameRequest={
            'playerId': player_id,
            'accountId': account_id
        }
    ).result()

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
