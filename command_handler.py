import helper
from room_storage import room_storage as rooms
from user_storage import user_storage as users
from room import Room


class CommandHandler:

    def __init__(self, bot):
        self.bot = bot

    def start(self, message):
        self.bot.send_message(chat_id=message.chat.id, text='Добро пожаловать в Jacknoon.')

    def find_room(self, message, room_id):
        bot_message = self.bot.send_message(chat_id=message.chat.id, text='Вы вошли в комнату ' + str(room_id) +
                                                                          + '\n' + rooms[room_id].info())
        rooms[room_id].add_player(message.from_user, bot_message, room_id)

    def create_room(self, message):
        room_id = helper.generate_id(rooms)
        rooms[room_id] = Room(room_id, message.from_user.id)
        self.bot.send_message(chat_id=message.chat.id, text='Комната создана.\nId комнаты - ' + str(room_id))
        self.find_room(message, room_id)

    def leave_room(self, message):
        player_id = message.from_user.id
        room_id = users[player_id]
        if rooms[room_id].owner != player_id:
            rooms[room_id].remove_player(player_id)
        else:
            rooms[room_id].__del__()
            rooms.pop(room_id)
        self.bot.send_message(chat_id=message.chat.id, text='Вы вышли в главное меню\n')
