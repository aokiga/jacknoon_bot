from bot_init import bot


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text=message.text[7:])


if __name__ == '__main__':
    running = True
    while running:
        bot.polling(none_stop=False)
