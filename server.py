# server.py

from flask import Flask, request
from flask_socketio import SocketIO, emit
from backend import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'div'
socketio = SocketIO(app)
backend = Game()

@socketio.on('connect')
def handle_connect():
    player_id = request.sid
    backend.connect_player(player_id)
    emit('update_players', backend.get_players(), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    player_id = request.sid
    backend.disconnect_player(player_id)
    emit('update_players', backend.get_players(), broadcast=True)

@socketio.on('set_player_position')
def handle_set_player_position(data):
    player_id = request.sid
    x = data['x']
    y = data['y']
    backend.set_player_position(player_id, x, y)
    emit('update_players', backend.get_players(), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost', port=5000)
