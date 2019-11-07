from telebot import types
from userState import UserState

keyboard_empty = types.ReplyKeyboardRemove(selective=False)

keyboard_main_menu = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
keyboard_main_menu.add(
    types.KeyboardButton('/create_room'),
    types.KeyboardButton('/enter_room'),
    types.KeyboardButton('/help')
)

keyboard_room = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
keyboard_room.add(
    types.KeyboardButton('/help'),
    types.KeyboardButton('/leave_room')
)

keyboard_game_mode = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
keyboard_game_mode.add(
    types.KeyboardButton('Смешная хуета'),
    types.KeyboardButton('Надо думать')
)

keyboards = {
    UserState.MAIN_MENU:             keyboard_main_menu,
    UserState.WAITING_FOR_ROOM_ID:   keyboard_empty,
    UserState.ROOM:                  keyboard_room,
    UserState.WAITING_FOR_GAME_MODE: keyboard_game_mode
}