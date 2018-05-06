import os

from bravado.client import SwaggerClient
from bravado.swagger_model import load_file

from game_service.constants import URLS

config = {
    'also_return_response': True,
    'validate_responses': True,
    'validate_requests': True,
    'validate_swagger_spec': True,
    'use_models': True,
    'formats': []
}

if os.environ.get('GAME_SERVICE_ENV') == 'local':
    env = 'local'
else:
    env= 'container'

account_service_client = SwaggerClient.from_spec(
    load_file(
        'swagger/account_service_api.yaml',
    ),
    origin_url=URLS[env].account_service,
    config=config
)

player_service_client = SwaggerClient.from_spec(
    load_file(
        'swagger/player_service_api.yaml',
    ),
    origin_url=URLS[env].player_service,
    config=config
)
