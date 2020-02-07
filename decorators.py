from bot_init import bot
from userState import UserState
from user_storage import users_state


def for_users(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if user_id not in users_state:
            bot.send_message(chat_id=message.chat.id, text='Введите /start')
            return
        func(message)

    return wrapped_handler


def for_users_free(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.MAIN_MENU:
            bot.send_message(chat_id=message.chat.id, text='Сначала выйдете в главное меню.')
            return
        func(message)

    return wrapped_handler


def for_users_room(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.ROOM:
            bot.send_message(chat_id=message.chat.id, text='Вы не находитесь в ожидании игры.')
            return
        func(message)

    return wrapped_handler


def for_users_game(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.GAME:
            return
        func(message)

    return wrapped_handler


def for_users_game_or_room(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] == UserState.MAIN_MENU:
            bot.send_message(chat_id=message.chat.id, text='Вы не находитесь в игре.')
            return
        func(message)

    return wrapped_handler


def for_users_election(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.ELECTION:
            return
        func(message)

    return wrapped_handler


def for_users_answer(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.ANSWER:
            return
        func(message)

    return wrapped_handler


def for_users_final_election(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.FINAL_ELECTION:
            return
        func(message)

    return wrapped_handler


def for_users_final_answer(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if users_state[user_id] != UserState.FINAL_ANSWER:
            return
        func(message)

    return wrapped_handler


def for_users_unregistered(func):
    def wrapped_handler(message):
        user_id = message.from_user.id
        if user_id in users_state:
            bot.send_message(chat_id=message.chat.id, text='Вы уже выполнили /start')
            return
        func(message)

    return wrapped_handler

