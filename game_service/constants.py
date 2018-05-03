from addict import Dict

URLS = Dict()
URLS.local.rdbs = 'postgresql+psycopg2://postgres:daleria@localhost:5432/game_service'
URLS.container.rdbs = 'postgresql+psycopg2://postgres:daleria@dukedoms-rdbs:5432/game_service'

URLS.local.account_service = 'http://localhost:5002'
URLS.container.account_service='http://account-service:5002'

URLS.local.player_service= 'http://localhost:5004'
URLS.container.player_service='http://player-service:5004'
