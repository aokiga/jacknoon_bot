from bot_init import bot
import decorators
from userState import UserState
from user_storage import users_room, users_state
from room_storage import room_storage as rooms

import command_handler


@bot.message_handler(commands=['start'])
@decorators.for_users_unregistered
def start(message):
    player_id = message.from_user.id
    users_state[player_id] = UserState.MAIN_MENU
    users_room[player_id] = 0
    command_handler.start(message)
    help_handler(message)


@bot.message_handler(commands=['help'])
@decorators.for_users
def help_handler(message):
    command_handler.help_bot(message)


@bot.message_handler(commands=['create_room'])
@decorators.for_users
@decorators.for_users_free
def create_game(message):
    command_handler.create_room(message)
    help_handler(message)


@bot.message_handler(commands=['enter_room'])
@decorators.for_users
@decorators.for_users_free
def connect(message):
    room_id = message.text[12::]
    if room_id not in rooms:
        bot.send_message(chat_id=message.chat.id, text='Некорректный id комнаты.')
        return
    command_handler.find_room(message, room_id)
    help_handler(message)


@bot.message_handler(commands=['leave_room'])
@decorators.for_users
@decorators.for_users_room
def leave_room(message):
    command_handler.leave_room(message)
    help_handler(message)


@bot.message_handler(commands=['say'])
@decorators.for_users
@decorators.for_users_game_or_room
def say(message):
    command_handler.say(message)


@bot.message_handler(commands=['begin_game'])
@decorators.for_users
@decorators.for_users_room
def begin_game(message):
    command_handler.begin_game(message)


if __name__ == '__main__':
    running = True
    while running:
        bot.polling(none_stop=False)
