from bot_init import bot
import decorators

import command_handler


@bot.message_handler(commands=['start'])
@decorators.for_users_unregistered
def start(message):
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
    command_handler.wait_for_id(message)
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


@bot.message_handler(func=lambda message: True)
@decorators.for_users
def parse_text(message):
    command_handler.parse_text(message)


if __name__ == '__main__':
    running = True
    while running:
        bot.polling(none_stop=False)
