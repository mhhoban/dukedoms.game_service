import json

from sqlalchemy import Column, Integer, JSON, String

from game_service.shared.db import Base

class GameState(Base):
    __tablename__ = 'game_state'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    active_player_id = Column(Integer)
    player_turn_order =Column(JSON)

    def __init__(self, game_id=None, player_turn_order=None, active_player_id=None):
        self.game_id = game_id
        self.player_turn_order = json.dumps({'playerTurnOrder': player_turn_order})
        self.active_player_id = active_player_id
