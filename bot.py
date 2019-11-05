from bot_init import bot
import decorators
from userState import UserState
from user_storage import users_room, users_state
from room_storage import room_storage as rooms

import command_handler

CommandHandler = command_handler.CommandHandler(bot)


@bot.message_handler(commands=['start'])
@decorators.for_unregistered_users
def start(message):
    player_id = message.from_user.id
    if player_id not in users_state:
        users_state[player_id] = UserState.MAIN_MENU
        users_room[player_id] = 0
        CommandHandler.start(message)
    help_handler(message)


@bot.message_handler(commands=['help'])
@decorators.for_existing_users
def help_handler(message):
    CommandHandler.help(message)


@bot.message_handler(commands=['create_room'])
@decorators.for_existing_users
@decorators.for_free_users
def create_game(message):
    CommandHandler.create_room(message)


@bot.message_handler(commands=['enter_room'])
@decorators.for_existing_users
@decorators.for_free_users
def connect(message):
    bot.send_message(chat_id=message.chat.id, text='Введите id комнаты.')
    users_state[message.from_user.id] = UserState.WAITING_FOR_ROOM_ID


@decorators.for_existing_users
@bot.message_handler(func=lambda message: users_state[message.from_user.id] == UserState.WAITING_FOR_ROOM_ID)
def enter_room_id(message):
    room_id = message.text
    if room_id not in rooms:
        bot.send_message(chat_id=message.chat.id, text='Комнаты с таким id не существует.')
        users_state[message.from_user.id] = UserState.MAIN_MENU
        return
    CommandHandler.find_room(message, room_id)


@bot.message_handler(commands=['leave_room'])
@decorators.for_existing_users
@decorators.for_busy_users
def leave_room(message):
    CommandHandler.leave_room(message)


if __name__ == '__main__':
    running = True
    while running:
        bot.polling(none_stop=False)
