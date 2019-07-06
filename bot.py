import os
import telebot

bot = telebot.TeleBot(os.getenv("TOKEN"))
telebot.apihelper.proxy = {'https':os.getenv("PROXY")}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello world!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()