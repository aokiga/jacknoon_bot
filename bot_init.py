import master_info
import telebot

TOKEN = master_info.TOKEN
PROXY = 'socks5://telegram:telegram@ogyom.tgvpnproxy.me:1080'
bot = telebot.TeleBot(TOKEN)
telebot.apihelper.proxy = {'https': PROXY}
