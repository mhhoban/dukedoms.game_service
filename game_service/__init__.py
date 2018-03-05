from flask import Flask, request
from game_service.shared.db import session, init_db

from game_service.models.game import Game

init_db()
app = Flask(__name__)

@app.route('/newGame', methods=['POST'])
def create_new_game():
    """
    Endpoint for creating new game
    """
    players = request.get_json()

    game_state = 'pending'
    new_game = Game(game_state=game_state, players=players)
    session.add(new_game)
    session.commit()
