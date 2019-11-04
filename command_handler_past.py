'''
def disconnect(player_id):
    game_storage[game_id].remove_player(player_id)
    if game_storage[game_id].empty():
        game_storage.pop(game_id)


def start_game(game_id):
    game_storage[game_id].play_game()
'''