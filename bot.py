import master_info
import telebot
import command_handler
from user_storage import user_storage as users
from room_storage import room_storage as rooms

TOKEN = master_info.TOKEN
PROXY = 'socks5h://telegram:telegram@ogyom.tgvpnproxy.me:1080'
bot = telebot.TeleBot(TOKEN)
telebot.apihelper.proxy = {'https': PROXY}

CommandHandler = command_handler.CommandHandler(bot)


@bot.message_handler(commands=['start'])
def start(message):
    player_id = message.from_user.id
    if player_id not in users:
        users[player_id] = 0
        CommandHandler.start(message)
    help_handler(message)


@bot.message_handler(commands=['help'])
def help_handler(message):
    CommandHandler.help(message)


@bot.message_handler(commands=['create_room'])
def create_game(message):
    player_id = message.from_user.id

    if player_id not in users:
        bot.send_message(chat_id=message.chat.id, text='Введите /start')
        return

    if users[player_id] != 0:
        bot.send_message(chat_id=message.chat.id, text='Вы уже находитесь в лобби. Сначала покиньте лобби.')
        return

    CommandHandler.create_room(message)


@bot.message_handler(commands=['enter_room'])
def connect(message):
    player_id = message.from_user.id
    
    if player_id not in users:
        bot.send_message(chat_id=message.chat.id, text='Введите /start.')
        return

    if users[player_id] != 0:
        bot.send_message(chat_id=message.chat.id, text='Вы уже находитесь в комнаты. Сначала покиньте комнату.')
        return

    bot.send_message(chat_id=message.chat.id, text='Введите id комнаты.')
    room_id = bot.get_updates(limit=1, allowed_updates=['message'])[0]

    if room_id not in rooms:
        bot.send_message(chat_id=message.chat.id, text='Комнаты с таким id не существует.')
        return

    CommandHandler.find_room(message, room_id)


'''
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

    сommand_handler.start_game(-user_storage[player_id])ч
'''

if __name__ == '__main__':
    running = True
    while running:
        bot.polling(none_stop=True)
