import telebot
import helper
from room_storage import room_storage as rooms
from user_storage import user_storage as users
from room import Room


class CommandHandler:

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def start(self, message):
        self.bot.send_message(chat_id=message.chat.id, text='Добро пожаловать в Jacknoon.')

    def help(self, message):
        self.bot.send_message(chat_id=message.chat.id, text='TODO()')
        # TODO() : need to output info following current condition

    def find_room(self, message, room_id):
        self.bot.send_message(chat_id=message.chat.id, text='Вы вошли в лобби\n' + rooms[room_id].info())
        rooms[room_id].add_player(message.from_user.id, message.chat.id, message.id)

    def create_room(self, message):
        room_id = helper.generate_id(rooms)
        rooms[room_id] = Room(room_id)
        self.bot.send_message(chat_id=message.chat.id, text='Комната создана.\nId комнаты - ' + str(room_id))
        self.find_room(message, room_id)
