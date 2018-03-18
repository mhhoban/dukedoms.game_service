class ActivePlayerId(Base):
    __tablename__ = 'active_player_ids'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    account_id = Column(Integer)
    player_id = Column(Integer)

    def __init__(self, game_id=None, account_id=None, player_id=None):
        self.game_id = game_id
        self.account_id = account_id
        self.player_id = player_id
