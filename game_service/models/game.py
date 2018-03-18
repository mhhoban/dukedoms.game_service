from sqlalchemy import Column, Integer, JSON, String

from game_service.shared.db import Base

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    game_state = Column(String(50))
    host_player = Column(JSON)
    accepted_players = Column(JSON)
    invited_players = Column(JSON)
    declined_players = Column(JSON)
    active_player = Column(Integer)

    def __init__(self, game_state=None, host_player=None, invited_players=None):
        self.game_state = game_state
        self.host_player = host_player
        self.invited_players = invited_players
