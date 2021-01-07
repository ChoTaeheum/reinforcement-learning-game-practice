from tkinter import *
import random
import csv
import time


# RANDOM_POS = [6*i for i in range(99)]
# random.shuffle(RANDOM_POS)
# print(RANDOM_POS)
# =============================

MAN_MOVE = [-6, 0, 6]

# 200개 로테이션
# RANDOM_POS = [501, 144, 360, 123, 420, 393, 519, 495, 45, 585, 189, 402, 309, 498, 171, 282, 366, 294, 234, 168, 426, 450, 261, 240, 429, 9, 231, 39, 306, 555, 579, 159, 423, 363, 558, 318, 150, 384, 348, 117, 204, 576, 27, 174, 525, 357, 63, 543, 255, 111, 141, 483, 273, 237, 480, 297, 48, 537, 570, 504, 279, 396, 36, 564, 552, 201, 0, 315, 459, 129, 588, 276, 198, 408, 465, 345, 183, 213, 75, 291, 186, 147, 405, 444, 60, 138, 561, 6, 399, 177, 69, 474, 264, 411, 3, 510, 195, 57, 72, 303, 513, 18, 546, 228, 165, 582, 333, 30, 531, 42, 87, 447, 390, 78, 567, 489, 381, 270, 96, 210, 219, 321, 126, 132, 387, 453, 84, 192, 528, 414, 330, 33, 66, 156, 369, 327, 468, 372, 456, 249, 207, 507, 153, 351, 435, 12, 516, 216, 246, 135, 375, 252, 288, 99, 24, 54, 522, 339, 432, 324, 114, 15, 120, 438, 102, 225, 573, 471, 534, 342, 285, 105, 417, 180, 300, 354, 108, 267, 462, 486, 81, 492, 21, 258, 336, 243, 540, 93, 441, 549, 477, 312, 51, 90, 378, 222, 162]

# 100개 로테이션
RANDOM_POS = [522, 312, 366, 78, 438, 276, 246, 552, 432, 90, 282, 330, 354, 186, 510, 48, 222, 120, 336, 132, 396, 30, 12, 294, 306, 144, 582, 42, 18, 342, 516, 36, 402, 126, 324, 450, 162, 6, 300, 408, 474, 168, 96, 180, 534, 252, 0, 318, 234, 60, 414, 348, 444, 174, 588, 486, 492, 66, 54, 150, 210, 498, 462, 372, 72, 504, 264, 426, 156, 558, 288, 192, 384, 378, 546, 138, 576, 240, 468, 390, 420, 102, 540, 84, 564, 570, 228, 24, 198, 258, 480, 216, 270, 360, 114, 108, 528, 456, 204]

KEY_VALUE = {}  # 좌표를 key으로, 가중치(Q)를 value로 갖는 딕셔너리


class Man_AI:
    DODGEPNT = 0

    def __init__(self, canvas):
        self.canvas = canvas
        self.man = canvas.create_rectangle(0, 0, 10, 20, fill='magenta')   # 왜 10으로 하면 안움직이는 걸까?
        self.canvas.move(self.man, 295, 480)  # self.man 그리기
        self.x = 0
        self.y = 0
        self.man_pos = self.canvas.coords(self.man)  # self.man의 좌상우하의 좌표, 위치 선언
        self.loadCSV()
        self.epsilon = 0   # 처음에는 랜덤 없이 시작  -->  5000바퀴 돌 때마다 랜덤유무 변환

    def draw(self):
        self.man_pos = self.canvas.coords(self.man)  # self.man의 좌상우하의 좌표, 위치 선언

        # self.man이 화면 밖으로 나가지 않도록 하는 코드
        if self.man_pos[0] <= 0 and self.x < 0:
            self.x = 6
        elif self.man_pos[2] >= 600 and self.x > 0:
            self.x = -6

        # random()에서 받은 속력값을 대입해서 self.man 그리기
        self.canvas.move(self.man, self.x, self.y)

    def move_choice(self, x):   # action()에 랜덤을 줄 때 사용
        rx = random.random()  # 0~1 사이의 값 반환
        if rx < self.epsilon:
            self.x = random.choice(MAN_MOVE)
        else:
            self.move(x)

    def move(self, x):
        # 랜덤으로 self.man이 움직일 속력 반환
        self.x = x


    def loadCSV(self):
        try:
            Fn = open("c:\\data\\poop_val-auto.csv", 'r')
            Poop.ROTATION_CNT = int(Fn.readline().split(',')[0])  # 첫 줄의 학습 게임 횟수 불러오기
            reader = csv.reader(Fn, delimiter=',')
            for key in reader:
                KEY_VALUE[(
                    int(float(key[0])), int(float(key[1])), int(float(key[2])),
                )] = float(key[3])
            print('Load Success! Start at rotation_cycle {0}'.format(Poop.ROTATION_CNT))
        except Exception:
            print('Load Failed!')

        try:
            Fn = Fn = open("c:\\data\\poop_score-auto.csv", 'r')
            reader = csv.reader(Fn, delimiter='\n')
            for score in reader:
                Poop.HIT_list.append(score[0])
        except Exception:
            print('Load score Failed!')


class Poop:
    CYCLE_DATA = []
    HIT = 0
    HIT_list = []
    ROTATION_CNT = 0

    def __init__(self, canvas, man, rdm_pos):  # append 되면서 실행
        self.get_point = 0  # 득점상황
        self.poop_x = 0  # self.poop의 x좌표
        self.man_x = 0  # self.man의 x좌표
        self.man_speed = 0  # self.man의 속력

        self.canvas = canvas
        self.man = man
        self.poop = canvas.create_oval(0, 0, 10, 10, fill='#E86A0C')  # 생성하기(그리기X)
        # self.poop = canvas.create_oval(0, 0, 10, 10, fill='pink')
        self.x = 0
        self.y = 6  # poop이 떨어지는 속도 조절
        self.random_pos = None
        self.learning = True
        self.alpha = 0.99  # 망각계수
        self.rdm_pos = rdm_pos
        self.random()
        self.canvas.move(self.poop, self.x_pos, 0)  # self.poop 그리기
        self.poop_pos = self.canvas.coords(self.poop)  # self.poop의 좌상우하의 좌표, 위치 선언
        self.direction = 0


    def random(self):  # 학습 결과 여기서 바꿔주면 됩니다.
        self.x_pos = self.rdm_pos


    def action(self):
        self.canvas.move(self.poop, self.x, self.y)  # 똥 그리기, self.poop_pos도 같이 update함

        if self.judgement_point():  # 여기서 결정된 행동이 기록된다.(는 줄 알았는데 첫놈만 들어간다.) 전체중에 하나씩 들어감(범위에 걸리는 놈)
            self.direction = self.greedy_choice()  # 처음에는 judgement_point()에 걸리지 않기 때문에 None을 반환한다.
            x = MAN_MOVE[self.direction]  # greedy_choice()에서 가장 적절한 items 번호 반환해서 사용
            self.man.move_choice(x)
            self.Qmaker()   # 가중치 계산


    def record(self):
        if self.judgement_point():  # 여기서 결정된 행동이 기록된다.(는 줄 알았는데 첫놈만 들어간다.) 전체중에 하나씩 들어감
            Poop.CYCLE_DATA.append(self.keystate(self.direction))  # greedy_choice에서 나온 값을 적용해서 append, 강화학습을 위한 데이터 저장


    def keystate(self, man_speed):  # 여기서 점수들을 판정해주고 판정당시의 정보들을 모아준다.
        if self.judgement_point():
            self.man_x = int(self.man.man_pos[0])
            self.man_speed = self.man.x
            self.poop_x = int(self.poop_pos[0])
            return (self.man_x, self.poop_x, man_speed)


    def judgement_point(self):  # 일정 높이에 도달했는지 판정
        self.poop_pos = self.canvas.coords(self.poop)

        # 득점 상황 선언
        if self.man.man_pos[1] <= self.poop_pos[3] <= self.man.man_pos[3] - 11:
            return True
        return False


    def hit_man(self):  # 일정 높이에 도달했을 때 맞았는지 안맞았는지 반환 ★★★★★★★★★★★★★★★★★★★★★★★★
        if self.man.man_pos[0] <= self.poop_pos[0] <= self.man.man_pos[2] \
                or self.man.man_pos[0] <= self.poop_pos[2] <= self.man.man_pos[2]:
            return True
        return False


    # Q를 계산해서 가장 적절한 값을 선택한다.
    def greedy_choice(self):  # 똥 하나에 세개의 값을 반환해서 KEY_VALUE에 쌓는다.
        val_left = self.keystate(0)  # 처음에는 judgement_point()에 안걸리기 때문에 None!
        val_stop = self.keystate(1)  # 처음에는 judgement_point()에 안걸리기 때문에 None!
        val_right = self.keystate(2)  # 처음에는 judgement_point()에 안걸리기 때문에 None!

        # Q 비교
        if self.lookup(val_left) > self.lookup(val_stop) \
                and self.lookup(val_left) > self.lookup(val_right):
            return 0
        elif self.lookup(val_stop) > self.lookup(val_left) \
                and self.lookup(val_stop) > self.lookup(val_right):
            return 1
        elif self.lookup(val_right) > self.lookup(val_left) \
                and self.lookup(val_right) > self.lookup(val_stop):
            return 2
        else:  # 적당한 값이 없을 경우, 즉 모두 0이거나 수가 같아서 비교가 불가능할 경우
            return random.choice([0, 1, 2])


    # 새로 들어온 key에 대한 value 지정 및 추가(add)
    def add(self, key):
        KEY_VALUE[key] = 0


    def lookup(self, key):
        if key not in KEY_VALUE:
            self.add(key)
        return KEY_VALUE[key]

    def reset_condition(self):
        if self.judgement_point():
            if self.hit_man():
                return True
        return False

    def reset(self):
        Poop.CYCLE_DATA = []  # 게임 끝나면 다시 Q값을 구해주기 위해 비워준다. for문에서 드르륵 여러번 선언, 상관없음
        # self.y = 1000

    def reinforcement(self, newVal, idx):
        if idx >= 0 and self.learning:
            preVal = round(KEY_VALUE[Poop.CYCLE_DATA[idx]], 5)  # 점수판정 바로 전의 데이터에 대한 Q값
            KEY_VALUE[Poop.CYCLE_DATA[idx]] += round((self.alpha * (newVal - preVal)),5)  # 결과가 일어나기 직전의 선택부터 차례대로 뒤로 가면서 가중치를 적용, 역전파 적용
            return self.reinforcement(newVal * self.alpha, idx - 1)  # 재귀

    def punishment(self, newVal, idx):
        if idx >= len(Poop.CYCLE_DATA) - 4 and self.learning:
            preVal = round(KEY_VALUE[Poop.CYCLE_DATA[idx]], 5)  # 점수판정 바로 전의 데이터에 대한 Q값
            KEY_VALUE[Poop.CYCLE_DATA[idx]] += round((self.alpha * (newVal - preVal)),
                                                     5)  # 결과가 일어나기 직전의 선택부터 차례대로 뒤로 가면서 가중치를 적용, 역전파 적용
            return self.punishment(newVal * self.alpha, idx - 1)  # 재귀

    def Qmaker(self):
        if Poop.ROTATION_CNT % 1000 == 0:  # save_term, csv파일에 담는 주기!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.writeCSV()

        if self.hit_man():
            Poop.HIT += 1
            result_value = -10  # 실패에 대한 보상치
            return self.punishment(result_value, len(Poop.CYCLE_DATA) - 2)

        else:
            result_value = 1  # 성공에 대한 보상치
            Man_AI.DODGEPNT += 1
            return self.reinforcement(result_value, len(Poop.CYCLE_DATA) - 2)

    def check_out(self):
        self.poop_pos = self.canvas.coords(self.poop)
        if self.poop_pos[3] >= 520:
            return True
        return False

    def writeCSV(self):
        Fn = open("c:\\data\\poop_val-auto.csv", 'w', newline='')
        writer = csv.writer(Fn, delimiter=',')  # 구분자 comma(csv파일 저장)
        writer.writerow([Poop.ROTATION_CNT])  # self.poop 한바퀴 돌때마다 저장
        keys = KEY_VALUE.keys()
        # print(keys)
        for key in keys:
            try:
                writer.writerow([
                    key[0],
                    key[1],
                    key[2],
                    KEY_VALUE[key]
                ])
            except:
                pass
        Fn.close()

        Fn = open("C:\\data\\poop_score-auto.csv", 'w', newline='')
        writer = csv.writer(Fn, delimiter=',')
        for HIT in Poop.HIT_list:
            writer.writerow([HIT])
        Fn.close()


    def __del__(self):
        return 'del'


tk = Tk()
tk.title("POOP DODGER!")  # 게임 창의 제목 출력
tk.resizable(0, 0)  # tk.resizable(가로크기조절, 세로크기조절)
tk.wm_attributes("-topmost", 1)  # 생성된 게임창을 다른창의 제일 위에 오도록 정렬
tk.update()  # 여기서 한번 다시 적어준다.

canvas = Canvas(tk, width=600, height=500, bd=0, highlightthickness=0)
# bd=0, highlightthickness=0 은 베젤의 크기를 의미한다.
canvas.configure(background='#E8D487')
canvas.pack()  # 앞의 코드에서 전달된 폭과 높이는 매개변수에 따라 크기를 맞추라고 캔버스에에 말해준다.

man = Man_AI(canvas)
poop = []   # 객체를 담을 리스트변수


while 1:
    Poop.ROTATION_CNT += 1


    # 랜덤 / 셀렉션 로테이션 모델@@@@@@@@@@@@
    if Poop.ROTATION_CNT % 1000 == 0:   # 랜덤 로테이션
        man.epsilon = 0
    elif Poop.ROTATION_CNT % 500 == 0:
        man.epsilon = 0.05

    # 랜덤 확률 감소 모델@@@@@@@@@@@@@@@@@@@
    # man.epsilon = 1 / (Poop.ROTATION_CNT+1)

    for rdm_pos in RANDOM_POS:

        tk.update()
        tk.update_idletasks()

        poop.append(Poop(canvas, man, rdm_pos))  # 객체 생성, Poop.POOP_X
        man.draw()

        for i in range(len(poop)):  # poop에 들어가있는 객체의 마지막 순서에 해당하는 객체의 메소드가 실행된다!
            try:
                poop[i].record()  # 객체 실행, 일부에서 judgement_point()가 걸린다.
                if poop[i].reset_condition():  # 전체에서 judgement_point()과 hit_man()이 걸린다.
                    poop[i].reset()
            except IndexError:
                continue

        for i in range(len(poop)):
            try:
                poop[i].action()
            except:
                continue


            if poop[i].check_out():
                canvas.delete(poop[i].poop)   # 이미지 삭제
                del poop[i]                   # 객체 삭제

            continue

        # time.sleep(0.015)   # 기호에 따라 쓰세요~~~!!!


    if Poop.ROTATION_CNT % 20 == 0:
        print('맞은횟수 :', Poop.HIT)  # Poop.judgement_point에 걸리지 않은 self.poop 고려
        print('rotation횟수(100개) :', Poop.ROTATION_CNT)
        # print('KEY_VALUE 데이터 개수 : {}/59700'.format(len(KEY_VALUE)))
        print('KEY_VALUE 데이터 개수 : {}/30000'.format(len(KEY_VALUE)))
        print('완성/랜덤혼합')
        print('===============================')
        Poop.HIT_list.append(Poop.HIT)
        Poop.HIT = 0

