import json

from game_service.models.game_state import GameState
from game_service.shared.db import get_new_db_session

class GameStateProxy:
    def __init__(self, game_id):
        self.game_id = game_id
        session = get_new_db_session()
        game_state = session.query(GameState).filter(GameState.game_id == game_id).first()
        self.player_turn_order = json.loads(game_state.player_turn_order)['playerTurnOrder']
        self.active_player_id = game_state.active_player_id

    def update_active_player_id(self, active_player_id):
        """
        updated active player id to given value
        """
        self.active_player_id = active_player_id
        session = get_new_db_session()
        session.query(GameState).filter(GameState.game_id == self.game_id).update(
            {'active_player_id': self.active_player_id}
        )
        session.commit()
        session.close()

    def get_next_player_email(self, current_player=None):
        """
        takes in email of current player, returns email of next player
        """

        # get next player index
        current_player_index = self.player_turn_order.index(current_player)
        next_player_index = None
        if current_player_index == (len(self.player_turn_order) - 1):
            next_player_index = 0
        else:
            next_player_index = current_player_index + 1

        return self.player_turn_order[next_player_index]
