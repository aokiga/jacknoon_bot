import os
import telebot
import command_handler
from user_storage import user_storage
from game_storage import game_storage

bot = telebot.TeleBot(os.getenv('TOKEN'))
telebot.apihelper.proxy = {'https': os.getenv('PROXY')}


@bot.message_handler(commands=['start'])
def start(message):
    player_id = message.from_user.id
    if player_id in user_storage:
        return
    user_storage[player_id] = 0
    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать в симулятор игры Jackbox Party Box.')


@bot.message_handler(commands=['create_game'])
def create_game(message):
    player_id = message.from_user.id

    if player_id not in user_storage:
        bot.send_message(chat_id=message.chat.id, text='Вы еще даже не ввели /start =(((((.')
        return

    if user_storage[player_id]:
        bot.send_message(chat_id=message.chat.id, text='Вы уже находитесь в игре.')
        return

    game_id = сommand_handler.create_game()
    bot.send_message(chat_id=message.chat.id, text='Игра создана.\nКлюч игры - ' + str(game_id))
    command_handler.connect(player_id, game_id)


@bot.message_handler(commands=['connect'])
def connect(message):
    player_id = message.from_user.id
    
    if player_id not in user_storage:
        bot.send_message(chat_id=message.chat.id, text='Вы еще даже не ввели /start =(((((.')
        return

    if user_storage[player_id] != 0:
        bot.send_message(chat_id=message.chat.id, text='Вы уже находитесь в игре. Сначала покиньте игру.')
        return

    game_id = 0

    bot.send_message(chat_id=message.chat.id, text='Введите ключ комнаты.')
    game_id = bot.get_updates(limit=1, allowed_updates=["message"])[0]

    if game_id not in game_storage[player_id]:
        bot.send_message(chat_id=message.chat.id, text='Игры с таким ключом не существует.')
        return

    сommand_handler.connect(player_id, game_id)


@bot.message_handler(commands=['disconnect'])
def disconnect(message):
    player_id = message.from_user.id

    if player_id not in user_storage:
        bot.send_message(chat_id=message.chat.id, text='Вы еще даже не ввели /start =(((((.')
        return

    if user_storage[player_id] == 0:
        bot.send_message(chat_id=message.chat.id, text='Вы не находитесь в игре.')
        return

    сommand_handler.disconnect(player_id)


@bot.message_handler(commands=['start_game'])
def start_game(message):
    player_id = message.from_user.id

    if player_id not in user_storage:
        bot.send_message(chat_id=message.chat.id, text='Вы еще даже не ввели /start =(((((.')
        return

    if user_storage[player_id] > 0:
        bot.send_message(chat_id=message.chat.id, text='Вы уже находитесь в игре. Сначала покиньте игру.')
        return

    if user_storage[player_id] == 0:
        bot.send_message(chat_id=message.chat.id, text='Вы не находитесь в зале ожидания.')
        return

    сommand_handler.start_game(-user_storage[player_id])


if __name__ == '__main__':
    bot.polling()
