from telebot import types
from userState import UserState

keyboard_empty = types.ReplyKeyboardRemove(selective=False)

keyboard_main_menu = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
keyboard_main_menu.add(
    types.KeyboardButton('/create_room'),
    types.KeyboardButton('/enter_room <id>'),
    types.KeyboardButton('/help')
)

keyboard_room = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
keyboard_room.add(
    types.KeyboardButton('/help'),
    types.KeyboardButton('/leave_room'),
    types.KeyboardButton('/say'),
)


keyboards = {
    UserState.MAIN_MENU:             keyboard_main_menu,
    UserState.ROOM:                  keyboard_room,
}