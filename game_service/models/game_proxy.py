import json

from game_service.models.game import Game
from game_service.shared.db import get_new_db_session
from game_service.shared.player_service_calls import register_pending_player

class GameProxy:
    def __init__(self, game_id):
        self.game_id=game_id
        session = get_new_db_session()
        game = session.query(Game).filter(Game.id == game_id).first()

        self.game_state = game.game_state
        self.host_player = game.host_player
        self.invited_players = json.loads(game.invited_players)['invitedPlayers']
        self.accepted_players = json.loads(game.accepted_players)['acceptedPlayers']
        self.declined_players = json.loads(game.declined_players)['declinedPlayers']
        self.pending_players = json.loads(game.pending_players)['pendingPlayers']
        self.player_ids = json.loads(game.player_ids)['playerIds']
        session.close()

    def get_player_id(self, player_email):
        """
        get player_id by player_email
        """
        return self.player_ids[player_email]

    def add_accepted_player(self, player_id=None, player_email=None, session=None, account_id=None):
        """
        add host player id directly to accepted players and player_ids
        """

        if not session:
            session = get_new_db_session()
        if not player_id:
            player_id = register_pending_player(game_id=self.game_id, account_id=account_id)

        self.accepted_players.append(player_email)
        self.player_ids[player_email] = player_id

        session.query(Game).filter(Game.id == self.game_id).update(
            {'accepted_players': json.dumps({'acceptedPlayers': self.accepted_players})}
        )
        session.query(Game).filter(Game.id == self.game_id).update(
            {'player_ids': json.dumps({'playerIds': self.player_ids})}
        )
        session.commit()
        session.close()

    def player_accepts_invite(self, player_email=None, game_id=None, account_id=None):
        """
        flow for removing given host_email from pending and adding to accepted
        """
        if not self.verify_player_pending(player_email):
            raise ValueError('PlayerNotPending')

        player_id = register_pending_player(game_id=game_id, account_id=account_id)

        session = get_new_db_session()

        self.remove_player_from_pending(player_email=player_email, session=session)
        self.add_accepted_player(player_id=player_id, player_email=player_email, session=session)

    def player_declines_invite(self, player_email=None):
        """
        flow for rejecting game participation
        """
        if not verify_player_pending(player_email):
            raise ValueError('PlayerNotPending')

        session = get_new_db_session()
        self.remove_player_from_pending(player_email=player_email, session=session)
        session.close()

    def remove_player_from_pending(self, player_email=None, session=None):
        """
        removes given player email from pending players list
        """
        self.pending_players.remove(player_email)
        session.query(Game).filter(Game.id == self.game_id).update(
            {'pending_players': json.dumps({'pendingPlayers': self.pending_players})}
        )

    def verify_player_pending(self, player_email):
        """
        verify if player submitting response is still pending
        """
        try:
            self.pending_players.index(player_email)
            return True
        except ValueError:
            return False

    def start_game_check(self):
        """
        returns True if there are no more pending players, false if there are still
        pending players
        """
        if len(self.pending_players) > 0:
            return False
        else:
            return True
