from addict import Dict

URLS = Dict()
URLS.local.rdbs = 'postgresql+psycopg2://dukedoms:daleria@localhost:5432/game_service'
URLS.container.rdbs = 'postgresql+psycopg2://dukedoms:daleria@dukedoms-rdbs:5432/game_service'
