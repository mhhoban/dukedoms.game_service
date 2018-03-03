from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/newGame', methods=['POST'])
def create_new_game():
    """
    Endpoint for creating new game
    """
    host_player = request.form['hostId']
    invited_players = request.form['invitedPlayers']
