import json

from game_service.models.game import GameState
from game_service.shared.db import get_new_db_session

class GameStateProxy:
    def __init__(game_id):
        self.game_id == game_id
        session = get_new_db_session()
        game_state = session.query(GameState).filter(GameState.game_id == game_id)
        self.player_turn_order = json.loads(game_state.player_turn_order)['playerTurnOrder']
        self.active_player_id = game_state.active_player_id
