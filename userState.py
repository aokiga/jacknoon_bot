from enum import Enum, auto


class UserState(Enum):
    MAIN_MENU = auto()
    ROOM = auto()
    GAME = auto()
    ELECTION = auto()
    ANSWER = auto()
