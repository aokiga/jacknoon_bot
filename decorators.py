from bot_init import bot
from user_storage import user_storage as users
from room_storage import room_storage as rooms


def for_existing_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if user_id not in users:
            bot.send_message(chat_id=message.chat.id, text='Введите /start')
            return
        func()
    return wrapped_handler


def for_free_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users[user_id] != 0:
            bot.send_message(chat_id=message.chat.id, text='Вы уже находитесь в комнате. Сначала покиньте комнату.')
            return
        func()
    return wrapped_handler


def for_busy_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users[user_id] != 0:
            bot.send_message(chat_id=message.chat.id, text='Вы не находитесь ни в какой комнате.')
            return
        func()
    return wrapped_handler
