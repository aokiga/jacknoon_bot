from bot_init import bot
import command_handler
import decorators
from user_storage import user_storage as users
from room_storage import room_storage as rooms

CommandHandler = command_handler.CommandHandler(bot)


@bot.message_handler(commands=['start'])
def start(message):
    player_id = message.from_user.id
    if player_id not in users:
        users[player_id] = 0
        CommandHandler.start(message)
    help_handler(message)


@bot.message_handler(commands=['help'])
@decorators.for_existing_users
def help_handler(message):
    bot.send_message(chat_id=message.chat.id, text='TODO()')
    # TODO() : need to output info following current condition


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
    room_id = bot.get_updates(limit=1, allowed_updates=['message'])[0].message.text

    if room_id not in rooms:
        bot.send_message(chat_id=message.chat.id, text='Комнаты с таким id не существует.')
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
