from bot_init import bot
from user_storage import user_storage as users


class Room:

    def __init__(self, room_id, owner_id):
        self.owner = owner_id
        self.players = dict()
        self.status_messages = dict()
        self.state = 0
        self.id = room_id

    def info(self):
        s = 'Количество игроков: ' + str(len(self.players)) + '\n'
        for player in self.players.values():
            s += player.username
        return s

    def update_status(self):
        new_text = self.info()
        for c_id, m_id in self.status_messages:
            bot.edit_message_text(text=new_text, chat_id=c_id, message_id=m_id)

    def add_player(self, player, message, game_id):
        self.players.update([(player.id, player)])
        self.status_messages.update([(player.id, (message.chat.id, message.message_id))])
        users[player.id] = game_id
        self.update_status()

    def remove_player(self, player_id):
        self.players.pop(player_id)
        self.status_messages.pop(player_id)
        users[player_id] = 0
        self.update_status()

    def close_game(self):
        players = self.players.keys()
        for player in players:
            self.remove_player(player)

    def empty(self):
        return not self.players
