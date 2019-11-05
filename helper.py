import random
from userState import UserState


def generate_id(rooms):
    key = 1
    while key in rooms:
        key = random.randint(1, 1e18)
    return key


helper = {
    UserState.MAIN_MENU: '''\
Вы находитесь в главном меню.
/help        - Список возможных команд
/create_room - Создать комнату
/enter_room  - Подключится к комнате 
''', UserState.WAITING_FOR_ROOM_ID: '''\
Введите Id комнаты, в которую хотите войти.
''', UserState.ROOM: '''\
Вы находитесь в комнате
/help       - Список возможных команд
/leave_room - Выйти из комнаты. Если вы создали комнату и выходите из нее, то она уничтожится.
''', UserState.WAITING_FOR_GAME_MODE: '''\
Выберите режим игры.
'''
}
