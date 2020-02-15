import random
from userState import UserState


def generate_id(rooms):  # i could also use mex() but i don't have much time for this
    key = 1
    while key in rooms:
        key = random.randint(1, 1e18)
    return str(key)


helper = {
    UserState.MAIN_MENU: '''\
Вы находитесь в главном меню.
/help            - Список возможных команд
/create_room     - Создать комнату
/enter_room      - Подключится к комнате
''',
    UserState.ROOM: '''\
Вы находитесь в комнате
/help       - Список возможных команд
/leave_room - Выйти из комнаты. Если вы создали комнату и выходите из нее, то она уничтожится.
/begin_game     - Начать игру
/say        - Отправить сообщение всем участникам
''',
    UserState.GAME: '''\
Вы находитесь в игре. Играйте!
/help       - Список возможных команд
/say        - Отправить сообщение всем участникам
''',
    UserState.ELECTION: '''\
Выберете нужное...
/help       - Список возможных команд
/say        - Отправить сообщение всем участникам
''',
    UserState.ANSWER: '''\
Эта штука вам в ответ запишется...
/help       - Список возможных команд
/say        - Отправить сообщение всем участникам
''',
    UserState.FINAL_ANSWER: '''\
Эта штука вам в ответ запишется...
/help       - Список возможных команд
/say        - Отправить сообщение всем участникам
''',
    UserState.FINAL_ELECTION: '''\
Выберете нужное...
/help       - Список возможных команд
/say        - Отправить сообщение всем участникам
''',
    UserState.ID: '''Введите id комнаты.'''
}
