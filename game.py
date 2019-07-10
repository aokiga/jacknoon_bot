from user_storage import *

import abc


class Game:

    def __init__(self, game_id):
        self.players = set()
        self.state = 0
        self.id = game_id

    def add_player(self, player_id):
        self.players.add(player_id)
        user_storage[player_id] = -self.id

    def remove_player(self, player_id):
        self.players.discard(player_id)
        user_storage[player_id] = 0

    def start_game(self):
        self.state = 1
        for player in self.players:
            user_storage[player] = self.id

    def play_game(self):
        self.start_game()
        self.finish_game()

    def finish_game(self):
        self.state = 0
        self.players = set()
        self.id = 0

    def empty(self):
        return not players
