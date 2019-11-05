from bot_init import bot
from userState import UserState
from user_storage import users_state
from room_storage import room_storage as rooms


def for_existing_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if user_id not in users_state:
            bot.send_message(chat_id=message.chat.id, text='Введите /start')
            return
        func(message)
    return wrapped_handler


def for_free_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.MAIN_MENU:
            bot.send_message(chat_id=message.chat.id, text='Сначала выйдете в главное меню.')
            return
        func(message)
    return wrapped_handler


def for_busy_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.ROOM and users_state[user_id] != UserState.GAME:
            bot.send_message(chat_id=message.chat.id, text='Вы не находитесь ни в какой комнате.')
            return
        func(message)
    return wrapped_handler


def for_unregistered_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if user_id in users_state:
            bot.send_message(chat_id=message.chat.id, text='Вы уже выполнили /start')
            return
        func(message)
    return wrapped_handler
