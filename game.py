from collections import OrderedDict, defaultdict
from time import sleep
from question import questions, final_questions
import random
from userState import UserState

intro_message = 'Добро пожаловать в игру Jacknoon.\nЗдесь нужно добавить красивое intro_message\n' \
                'В этом раунде Вам будут даны два вопроса и вы должны наиболее \'смешно\'(лол, нет) на них ' \
                'ответить.\nПосле этого игроки будут голосовать за лучший ответ. '
round_message = 'В этом раунде будут серьезные перемены в правилах. Он такой же, но очков в два.раза ' \
                 'больше.\nПогнали. '
final_round_message = 'Игра почти подошла к концу, но еще не все потеряно! Можно потерять еще больше! В финальном ' \
                      'раунде всем игрокам надо будет ответить на один вопрос.\n Поехали. '
final_message = 'Игра закончена.\n Всем спасибо за внимание.\nИ, да, у нас есть победитель и это - '

used_questions = set()


def generate_question_num():
    key = random.randint(0, len(questions) - 1)
    while key in used_questions:
        key = random.randint(0, len(questions) - 1)
    return key


class Game:
    def __init__(self, room):
        self.room = room
        self.room.set_state(UserState.GAME)
        self.score = OrderedDict(map((lambda x: (x, 0)), self.room.players.keys()))
        self.n = len(self.score)
        self.answers = defaultdict()  # (player_id, question_num) -> answer
        self.player_questions = defaultdict()
        self.player_questions.update(map((lambda x: (x, [])), self.room.players.keys()))  # player_id -> [q1, q2]
        self.player_answered = defaultdict()  # player_id -> num
        self.player_answered.update(map((lambda x: (x, 0)), self.room.players.keys()))
        self.current_questions = []
        self.final_answers = defaultdict()
        self.e1 = []
        self.e2 = []
        self.final_scoring = OrderedDict(map((lambda x: (x, 0)), self.room.players.keys()))
        self.final_question = 0
        self.medals_given = defaultdict()
        self.medals_given.update(map((lambda x: (x, 0)), self.room.players.keys()))
        self.ready = set()

    def _wait(self, sec):
        for _ in range(sec):
            sleep(1)
            if len(self.ready) == self.n:
                return 1
        return 0

    def wait(self):
        if self._wait(30):
            return
        self.room.send_message('Осталось 60 секунд...')
        if self._wait(30):
            return
        self.room.send_message('Осталось 30 секунд...')
        if self._wait(20):
            return
        self.room.send_message('Осталось 10 секунд...')
        if self._wait(10):
            return

    def common_answering(self):
        self.room.set_state(UserState.ANSWER)
        players = list(self.room.players.keys())
        shift = random.randint(1, len(players) - 1)
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
        self.room.set_state(UserState.GAME)

    def game_round(self, basic_score):
        self.common_answering()
        self.election(basic_score)
        self.current_questions = []
        self.ready = set()
        self.player_questions = defaultdict()
        self.player_questions.update(map((lambda x: (x, [])), self.room.players.keys()))
        self.player_answered = defaultdict()  # player_id -> num
        self.player_answered.update(map((lambda x: (x, 0)), self.room.players.keys()))

    def final_round(self):
        self.room.set_state(UserState.FINAL_ANSWER)
        self.final_question = random.randint(0, len(final_questions) - 1)
        self.room.send_message(final_questions[self.final_question])
        self.wait()
        self.final_election()
        self.ready = set()

    def get_answer(self, player_id, qnum):
        if (player_id, qnum) in self.answers:
            return self.answers[(player_id, qnum)]
        else:
            return "Нет ответа..."

    def show_res_election(self, pl, qnum, basic_score, arr):
        p = basic_score * (len(arr)) / (len(self.e1) + len(self.e2))
        res = ('@' + self.room.players[pl].username + ': ' + self.get_answer(pl, qnum) + '\n')
        res += (str(len(arr)) + ' votes: ' + ', '.join(
            map((lambda x: '@' + self.room.players[x].username), arr)) + '\n')
        res += ('+ ' + str(p) + ' points\n')
        self.score[pl] += p
        return res

    def put_answer(self, player_id, text):
        if self.player_answered[player_id] == 2:
            self.room.send_user(player_id, 'Вы уже ответили на все вопросы.')
            return
        if self.player_answered[player_id] == 1:
            qnum = self.player_questions[player_id][1]
            self.room.send_user(player_id, 'Спасибо за ответы.')
            self.answers[(player_id, qnum)] = text
            self.player_answered[player_id] += 1
            self.ready.add(player_id)
        if self.player_answered[player_id] == 0:
            qnum = self.player_questions[player_id][0]
            self.room.send_user(player_id, questions[self.player_questions[player_id][1]])
            self.answers[(player_id, qnum)] = text
            self.player_answered[player_id] += 1

    def election(self, basic_score):
        self.room.set_state(UserState.ELECTION)
        random.shuffle(self.current_questions)
        self.room.send_message("Напишите 1 или 2, чтобы отдать ваш голос")
        for qnum, pl1, pl2 in self.current_questions:
            self.room.send_message(questions[qnum])
            sleep(1)
            self.room.send_message('1 : ' + self.get_answer(pl1, qnum) + '\n' +
                                   '2 : ' + self.get_answer(pl2, qnum))
            self.e1 = []
            self.e2 = []
            self.ready = set()
            self._wait(30)
            results = self.show_res_election(pl1, qnum, basic_score, self.e1) + \
                      self.show_res_election(pl2, qnum, basic_score, self.e2)
            self.room.send_message(results)
        self.room.set_state(UserState.GAME)

    def get_final_answer(self, player_id):
        if player_id in self.final_answers:
            return self.final_answers[player_id]
        else:
            return "Нет ответа..."

    def final_election(self):
        self.room.set_state(UserState.FINAL_ELECTION)
        self.room.send_message(final_questions[self.final_question])
        sleep(2)
        self.room.send_message('\n'.join(map((lambda ix: str(ix[0]) + ': ' + self.get_final_answer(ix[1])),
                                             enumerate(self.score.keys()))))
        self.room.send_message('Введите номер ответа, которому вы хотите отдать ЗОЛОТУЮ МЕДАЛЬ (3 ФП).')
        self.ready = set()
        self._wait(80)
        self.final_scoring = OrderedDict(reversed(sorted(self.final_scoring.items(), key=(lambda x: x[1]))))
        res = ''
        n = len(self.score)
        order = list(self.final_scoring.items())
        for i in range(self.n):
            player_id, score = order[i]
            self.score[player_id] += (n - i) * 500
            res += '@' + self.room.players[player_id].username + ': ' + self.get_final_answer(player_id) + '\n' + \
                   str(score) + ' ФП, + ' + str((n - i) * 500) + 'points\n'
        self.room.send_message(res)
        self.room.set_state(UserState.GAME)

    def put_final_voice(self, player_id, text):
        if not text.isdigit() or int(text) >= self.n:
            return
        voice = int(text)
        players = list(self.score.keys())
        if self.player_answered[player_id] == 3:
            self.room.send_user(player_id, 'Вы уже отдали все медали.')
            return
        if self.player_answered[player_id] == 2:
            self.final_scoring[players[voice]] += 1
            self.room.send_user(player_id, 'Спасибо за медали.')
            self.player_answered[player_id] += 1
            self.ready.add(player_id)
        if self.player_answered[player_id] == 1:
            self.final_scoring[players[voice]] += 2
            self.room.send_user(player_id, 'Теперь выберите человека, которому мы дадите БРОНЗОВУЮ медаль (1 ФП).\n'
                                           '(P.S не выбирайте, пожалуйста, одного и того же человека второй раз. ')
            self.player_answered[player_id] += 1
        if self.player_answered[player_id] == 0:
            self.final_scoring[players[voice]] += 3
            self.room.send_user(player_id, 'Теперь выберите человека, которому мы дадите СЕРЕБРЯНУЮ медаль (2 ФП).\n'
                                           '(P.S не выбирайте, пожалуйста, одного и того же человека второй раз.')
            self.player_answered[player_id] += 1

    def put_final_answer(self, player_id, text):
        if player_id in self.final_answers:
            return
        self.final_answers[player_id] = text
        self.room.send_user(player_id, 'Спасибо за ответы.')
        self.ready.add(player_id)

    def put_voice(self, player_id, text):
        if text != '1' and text != '2':
            self.room.send_user(player_id, 'Некорректный ввод. Введите 1 или 2')
            return
        if player_id in self.e1 or player_id in self.e2:
            return
        if text == '1':
            self.e1.append(player_id)
        if text == '2':
            self.e2.append(player_id)
        self.ready.add(player_id)

    def play(self):
        self.room.send_message(intro_message)
        sleep(5)
        self.game_round(1000)
        sleep(5)
        self.show_results()
        sleep(5)
        self.room.send_message(round_message)
        sleep(5)
        self.game_round(2000)
        sleep(5)
        self.show_results()
        sleep(5)
        self.room.send_message(final_round_message)
        sleep(5)
        self.final_round()
        sleep(5)
        self.show_results()
        self.room.send_message(final_message + self.choose_winner())

    def choose_winner(self):
        for info in self.score.keys():
            return '@' + self.room.players[info].username

    def show_results(self):
        results = 'Раунд подошел к концу.\nТекущие результаты:\n'
        self.score = OrderedDict(reversed(sorted(self.score.items(), key=(lambda x: x[1]))))
        for player_id, score in self.score.items():
            results += '@' + self.room.players[player_id].username + ': ' + str(score) + '\n'
        self.room.send_message(results)
