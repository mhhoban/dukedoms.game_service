from sqlalchemy import Column, Integer, JSON, String

from game_service.shared.db import Base

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    game_state = Column(String(50))
    players = Column(JSON)

    def __init__(self, game_state=None, players=None):
        self.game_state = game_state
        self.players = players
