from enum import Enum, auto


class UserState(Enum):
    MAIN_MENU = auto()
    WAITING_FOR_ROOM_ID = auto()
    ROOM = auto()
    WAITING_FOR_GAME_MODE = auto()
    GAME = auto()
