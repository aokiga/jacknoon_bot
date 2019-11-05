import master_info
import telebot

TOKEN = master_info.TOKEN
PROXY = master_info.PROXY
bot = telebot.TeleBot(TOKEN)
telebot.apihelper.proxy = {'https': PROXY}
