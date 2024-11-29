# backend.py

class Game:
    def __init__(self):
        self.players = {}

    def connect_player(self, player_id):
        self.players[player_id] = {'x': 375, 'y': 375}

    def disconnect_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def get_players(self):
        return self.players

    def set_player_position(self, player_id, x, y):
        if player_id in self.players:
            self.players[player_id]['x'] = x
            self.players[player_id]['y'] = y
