from collections import defaultdict

from bot_init import bot
from user_storage import users_room, users_state
from userState import UserState


class Room:

    def __init__(self, room_id, owner_id):
        self.owner = owner_id
        self.players = defaultdict()
        self.status_messages = defaultdict()
        self.state = 0
        self.id = room_id

    def info(self):
        s = 'Количество игроков: ' + str(len(self.players)) + '\n'
        for player in self.players.values():
            s += '@' + player.username + '\n'
        return s

    def update_status(self):
        new_text = self.info()
        for c_id, m_id in self.status_messages.values():
            bot.edit_message_text(text=new_text, chat_id=c_id, message_id=m_id)

    def add_player(self, player, message, room_id):
        self.players.update([(player.id, player)])
        self.status_messages.update([(player.id, (message.chat.id, message.message_id))])
        users_room[player.id] = room_id
        users_state[player.id] = UserState.ROOM
        self.update_status()

    def remove_player(self, player_id):
        self.players.pop(player_id)
        self.status_messages.pop(player_id)
        users_room[player_id] = 0
        users_state[player_id] = UserState.MAIN_MENU
        self.update_status()

    def kick_player(self, player_id):
        bot.send_message(chat_id=self.status_messages[player_id][0],
                         text='Вы были кикнуты из комнаты,')
        self.remove_player(player_id)

    def close_game(self):
        while len(self.players) != 0:
            player_id, info = self.status_messages.popitem()
            self.players.pop(player_id)
            users_room[player_id] = 0
            users_state[player_id] = UserState.MAIN_MENU
            bot.send_message(chat_id=info[0], text='Вы были кикнуты из комнаты, так как она была уничтожена.')

    def empty(self):
        return not self.players

    def set_state(self, state):
        for player_id, info in self.status_messages:
            users_state[player_id] = state

    def send_message(self, text):
        for c_id, _ in self.status_messages.values():
            bot.send_message(chat_id=c_id, text=text)

    def send_user(self, player_id, text):
        bot.send_message(chat_id=self.status_messages[player_id][0], text=text)

    def get_number_of_players(self):
        return len(self.players)