from room_storage import room_storage as rooms
from user_storage import user_storage as users


class Room:

    def __init__(self, room_id):
        self.players = set()
        self.state = 0
        self.id = room_id

    def add_player(self, player_id):
        self.players.add(player_id)
        users[player_id] = -self.id

    def remove_player(self, player_id):
        self.players.discard(player_id)
        users[player_id] = 0

    def start_game(self):
        self.state = 1
        for player in self.players:
            users[player] = self.id

    def play_game(self):
        self.start_game()
        self.finish_game()

    def finish_game(self):
        self.state = 0
        self.players = set()
        self.id = 0

    def empty(self):
        return not self.players
