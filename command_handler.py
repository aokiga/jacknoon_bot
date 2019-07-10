from game import Game
from user_storage import user_storage
from game_storage import game_storage
import random


def generate_key():
    key = 0
    while key in games:
        key = random.randint(1, 1e18)
    return key


def create_game():
    key = generate_key()
    game_storage.update(key, Game(key))
    return key


def connect(player_id, game_id):
    game_storage[game_id].add_player(player_id)


def disconnect(player_id):
    game_storage[game_id].remove_player(player_id)
    if game_storage[game_id].empty():
        game_storage.pop(game_id)


def start_game(game_id):
    game_storage[game_id].play_game()
