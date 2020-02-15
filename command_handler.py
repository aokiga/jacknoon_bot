import helper
from bot_init import bot
from room_storage import room_storage as rooms
from game_storage import game_storage as games
from user_storage import users_room, users_state
from room import Room
from game import Game
from userState import UserState


def start(message):
    player_id = message.from_user.id
    users_state[player_id] = UserState.MAIN_MENU
    users_room[player_id] = 0
    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать в Jacknoon.')


def find_room(message):
    room_id = message.text
    player_id = message.from_user.id
    if room_id not in rooms:
        bot.send_message(chat_id=message.chat.id, text='Некорректный id комнаты.')
        users_state[player_id] = UserState.MAIN_MENU
        help_bot(message)
        return
    bot.send_message(chat_id=message.chat.id, text='Вы вошли в комнату ' + str(room_id))
    _enter_room(message, room_id)
    help_bot(message)


def create_room(message):
    room_id = helper.generate_id(rooms)
    rooms[room_id] = Room(room_id, message.from_user.id)
    bot.send_message(chat_id=message.chat.id, text='Комната создана.\nId комнаты - ' + str(room_id))
    _enter_room(message, room_id)


def _enter_room(message, room_id):
    bot_message = bot.send_message(chat_id=message.chat.id, text=rooms[room_id].info())
    rooms[room_id].add_player(message.from_user, bot_message, room_id)


def leave_room(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    if rooms[room_id].owner != player_id:
        rooms[room_id].remove_player(player_id)
    else:
        rooms[room_id].close_game()
        rooms.pop(room_id)
    bot.send_message(chat_id=message.chat.id, text='Вы вышли в главное меню\n')


def help_bot(message):
    state = users_state[message.from_user.id]
    bot.send_message(chat_id=message.chat.id,
                     text=helper.helper[state])


def say(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    rooms[room_id].send_message('@' + message.from_user.username + ' кричит:\n' + message.text[5:])


def begin_game(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    if rooms[room_id].get_number_of_players() == 1:
        rooms[room_id].send_message("Слишком мало игроков для создания игры.")
        return
    games[room_id] = Game(rooms[room_id])
    games[room_id].play()
    games.pop(room_id)
    rooms[room_id].set_state(UserState.ROOM)


def answer(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    games[room_id].put_answer(player_id, message.text)


def put_voice(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    games[room_id].put_voice(player_id, message.text)


def final_answer(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    games[room_id].put_final_answer(player_id, message.text)


def final_voice(message):
    player_id = message.from_user.id
    room_id = users_room[player_id]
    games[room_id].put_final_voice(player_id, message.text)


def parse_text(message):
    player_id = message.from_user.id
    if users_state[player_id] == UserState.ID:
        find_room(message)
    elif users_state[player_id] == UserState.ANSWER:
        answer(message)
    elif users_state[player_id] == UserState.ELECTION:
        put_voice(message)
    elif users_state[player_id] == UserState.FINAL_ANSWER:
        final_answer(message)
    elif users_state[player_id] == UserState.FINAL_ELECTION:
        final_voice(message)


def wait_for_id(message):
    player_id = message.from_user.id
    users_state[player_id] = UserState.ID
