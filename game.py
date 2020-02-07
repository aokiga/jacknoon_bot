from collections import OrderedDict, defaultdict
from time import sleep
from question import questions, final_questions
import random

intro_message = 'Добро пожаловать в игру Jacknoon.\nЗдесь нужно добавить красивое intro_message, но мне похуй, реально.'
round1_message = 'В этом раунде Вам будут даны два вопроса и вы должны наиболее \'смешно\'(лол, нет) на них ' \
                 'ответить.\nПосле этого игроки будут голосовать за лучший ответ. '
round2_message = 'В этом раунде будут серьезные перемены в правилах. Он такой же, но очков в два.сука.раза ' \
                 'больше.\nПогнали. '
final_round_message = 'Игра почти подошла к концу, но еще не все потеряно! Можно потерять еще больше! В финальном ' \
                      'раунде всем игрокам надо будет ответить на один вопрос.\n Поехали. '
final_message = 'Игра закончена.\n Всем спасибо за внимание.\nИ, да, у нас есть победитель (главный еблан) и это - '

used_questions = set()


def generate_question_num():
    key = random.randint(0, len(questions) - 1)
    while key in used_questions:
        key = random.randint(0, len(questions) - 1)
    return key


class Game:
    def __init__(self, room):
        self.room = room
        self.room.init_game()
        self.score = OrderedDict(map((lambda x: (x, 0)), self.room.players.keys()))
        self.answers = defaultdict()  # (player_id, question_num) -> answer
        self.player_questions = defaultdict()
        self.player_questions.update(map((lambda x: (x, [])), self.room.players.keys()))  # player_id -> [q1, q2]
        self.player_answered = defaultdict()  # player_id -> num
        self.current_questions = []

    def wait(self):
        self.room.send_message('Осталось 90 секунд...')
        sleep(30)
        self.room.send_message('Осталось 60 секунд...')
        sleep(30)
        self.room.send_message('Осталось 30 секунд...')
        sleep(20)
        self.room.send_message('Осталось 10 секунд...')
        sleep(10)
        self.room.send_message('Ответы больше не принимаются.')

    def game_round(self, basic_score):
        players = self.room.players.keys()
        shift = random.randint(1, len(players) - 1)
        for _ in range(2):
            for i, player_id in enumerate(players):
                qnum = generate_question_num()
                used_questions.add(qnum)
                other_player = players[(i + shift) % len(players)]
                self.current_questions.append((qnum, player_id, other_player))
                self.player_questions[player_id].append(qnum)
                self.player_questions[other_player].append(qnum)
        for player_id in players:
            self.room.send_user(player_id, questions[self.player_questions[player_id][0]])
        self.wait()
        random.shuffle(self.current_questions)
        self.election()
        self.current_questions = []
        self.player_questions = map((lambda x: (x, [])), self.room.players.keys())

    def final_round(self):
        qnum = random.randint(0, len(final_questions) - 1)
        self.room.send_message(final_questions[qnum])
        self.wait()
        self.final_election()

    def election(self):
        pass

    def final_election(self):
        pass

    def play(self):
        self.room.send_message(intro_message)
        sleep(4)
        self.room.send_message(round1_message)
        sleep(10)
        self.game_round(1000)
        sleep(3.14)
        self.show_results()
        sleep(10)
        self.room.send_message(round2_message)
        sleep(10)
        self.game_round(2000)
        sleep(3.14)
        self.show_results()
        sleep(10)
        self.room.send_message(final_round_message)
        sleep(10)
        self.final_round()
        sleep(3.14)
        self.show_results()
        self.room.send_message(final_round_message + self.choose_winner())

    def choose_winner(self):
        for info in self.score.keys():
            return '@' + self.room.players[info[0]].username

    def show_results(self):
        results = 'Раунд подошел к концу.\nТекущие результаты:\n'
        self.score = sorted(self.score)
        for player_id, score in self.score:
            results += '@' + self.room.players[player_id].username + ': ' + score + '\n'
        self.room.send_message(results)
