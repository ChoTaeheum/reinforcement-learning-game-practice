from tkinter import *
import random
import time

class Ball:

    def __init__(self, canvas, paddle, paddle1, color):  #공의 크기와 색깔
        self.canvas = canvas
        self.paddle = paddle        #서, 남, 동, 북
        self.paddle1 = paddle1
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        canvas.configure(background='black') #캔버스의 색깔 검정색으로.., configure - 환경설정
        self.canvas.move(self.id, 245, 100)  #공의 위치(공, x축, y축 - 위부터)
        starts = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]       #처음 움직이는 공의 방향 - 왼쪽부터
        random.shuffle(starts)               #stats를 섞는다.

        self.x = starts[0]    #속력
        #self.x = random.choice(starts)      #choice함수도 사용가능
        self.y = -5   #숫자가 크면 클수록 더 빨리 간다.
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False              #바닥에 닿으면 게임이 끝나는 코드, False로 초기화

    #     self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
    #     self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
    #
    #     self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
    #     self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
        self.canvas.bind_all('<space>', self.turn_up)    #'<Key>' == any key
    #
    # def turn_left(self,evt):
    #     self.x = -9
    #
    # def turn_right(self,evt):
    #     self.x = 9
    #
    # def turn_up(self,evt):
    #     self.y = -9

    def turn_up(self,evt):

        starts = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]       #처음 움직이는 공의 방향 - 왼쪽부터
        random.shuffle(starts)               #stats를 섞는다.

        self.x = starts[0]
        #self.x = random.choice(starts)      #choice함수도 사용가능
        self.y = -7   #숫자가 크면 클수록 더 빨리 간다.
    #
    # def turn_down(self,evt):
    #     self.y = 9
    #
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)  #공을 움직이게 하는 함수(공, 좌우방향, 상하방향)




        pos = self.canvas.coords(self.id)
        # print(pos)
        if pos[1] <= 0:                              #천정
            self.y = 7
        # if pos[3] >= self.canvas_height:
        #     self.hit_bottom = True                 #pass 게임 끝
        if pos[3] >= self.canvas_height:
            # print('miss다 miss')                     #바닥
            self.y = -7
        if pos[0] <= 0:                              #왼쪽 벽
            self.x = 7
        if pos[2] >= self.canvas_width:              #오른쪽 벽
            self.x = -7
        # if self.hit_paddle(pos) == True:             #공이 패들이 부딪히면 위로 튀겨라라
        #    self.y = 0
        #    self.x = 0                                #공이 멈추게 하기

        if self.hit_paddle1(pos) == True:             #공이 패들이 부딪히면 위로 튀겨라라
            self.y = -7

        if self.hit_paddle2(pos) == True:
            self.y = 7

        if self.hit_paddle3(pos) == True:  # 공이 패들이 부딪히면 위로 튀겨라라
            self.y = -7

        if self.hit_paddle4(pos) == True:
            self.y = 7

        # if 405 >= pos[3] >= 400:
        #     # print('miss')
        #     return
                                                     #공이 패들에 붙게 하는거
        # if self.hit_paddle2(pos) == True:
        #     self.y = 9
        #     return







        # if self.hit_paddle(pos) == True:             #공이 패들이 부딪히면 위로 튀겨라라
        #    self.y = -3
        # print(pos)
        #[110.0, 1331.0, 125.0, 1346.0](서쪽, 북쪽, 동쪽, 남쪽) 좌표

    def hit_paddle1(self,pos):
        global paddle_pos
        paddle_pos = self.canvas.coords(self.paddle.id)               #패들의 위치를 조회하는 코드
        if pos[2] >= paddle_pos[0]-7 and pos[0] <= paddle_pos[2]+7:       #공이 패들 옆면에 부딪혔을 때
            if paddle_pos[1]-2 <= pos[3] < paddle_pos[1]+5:
                # print('hit다 hit!')    #공이 패들 윗면의 부딪혔을 때
                return True
        # rint('miss다 miss!')
        return False

    def hit_paddle2(self, pos):
        if pos[2] >= paddle_pos[0]-7 and pos[0] <= paddle_pos[2]+7:
            if paddle_pos[3]-5 <= pos[1] <= paddle_pos[3]+2:
                return True
        return False

    def hit_paddle3(self, pos):  #paddle1 위에서 밑으로
        global paddle1_pos
        paddle1_pos = self.canvas.coords(self.paddle1.id)
        if pos[2] >= paddle1_pos[0]-7 and pos[0] <= paddle1_pos[2]+7:
            if paddle1_pos[1]-2 <= pos[3] <= paddle1_pos[1]+5:
                # print('hit다 hit!')
                return True
        # rint('miss다 miss!')
        return False

    def hit_paddle4(self, pos):  #paddle1 밑에서 위로
        if pos[2] >= paddle1_pos[0]-7 and pos[0] <= paddle1_pos[2]+7:
            if paddle1_pos[3]-5 < pos[1] <= paddle1_pos[3]+2:
                return True
        return False

    # def hit_paddle2(self,pos):
    #     global paddle_pos
    #     paddle_pos = self.canvas.coords(self.paddle.id)               #패들의 위치를 조회하는 코드
    #     if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:       #공이 패들 옆면에 부딪혔을 때
    #         if pos[1] == paddle_pos[3]:   #공이 패들 아래면의 부딪혔을 때
    #             return True
    #     # rint('miss다 miss!')
    #     return False
    #
    # def gameover(self):
    #     if self.y >= 400:
    #         print('miss')


class Paddle:

    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10,fill=color)
        self.canvas.move(self.id, 250, 420)   #패들을 움직이게 하는 함수
        self.x = 0                            #게임 시작할 때 패들이 움직이지 말라고 고정
        self.y = 0
        self.canvas_width = self.canvas.winfo_width()   #패들이 화면 바깥으로 나가지 않게
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)    #turn_left 함수와 바인딩
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)  #turn_right 함수와 바인딩
        # self.canvas.bind_all('<KeyPress-Up>',self.turn_up)
        # self.canvas.bind_all('<KeyPress-Down>',self.turn_down)

    def draw(self):

        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 and self.x < 0:
            self.x = 7

        elif pos[2] >= self.canvas_width and self.x > 0:
            self.x = -7

        self.canvas.move(self.id, self.x, self.y)

    def turn_left(self,evt):
        self.x = -7

    def turn_right(self,evt):
        self.x = 7

    # def turn_up(self,evt):
    #     self.y = -9
    #
    # def turn_down(self,evt):
    #     self.y = 9

class Paddle1:
    def __init__(self,canvas,color):

        self.canvas = canvas
        self.id = canvas.create_rectangle(100,0,0,10,fill=color)
        self.canvas.move(self.id, 250, 80)   #패들을 움직이게 하는 함수
        self.x = 5                           #게임 시작할 때 패들이 움직이지 말라고 고정
        self.y = 0
        self.canvas_width = self.canvas.winfo_width()   #패들이 화면 바깥으로 나가지 않게
        self.canvas_height = self.canvas.winfo_height()
        # self.canvas.bind_all('<KeyPress-Left>',self.turn_left)    #turn_left 함수와 바인딩
        # self.canvas.bind_all('<KeyPress-Right>',self.turn_right)  #turn_right 함수와 바인딩
        # self.canvas.bind_all('<KeyPress-Up>',self.turn_up)
        # self.canvas.bind_all('<KeyPress-Down>',self.turn_down)

    def draw(self):

        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 and self.x < 0:
            self.x = 7

        elif pos[2] >= self.canvas_width and self.x > 0:
            self.x = -7

        self.canvas.move(self.id, self.x, self.y)

    # def turn_left(self,evt):
    #     self.x = -5
    #
    # def turn_right(self,evt):
    #     self.x = 5

    # def turn_up(self,evt):
    #     self.y = -9
    #
    # def turn_down(self,evt):
    #     self.y = 9

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)

canvas = Canvas(tk, width=600, height=500, bd=0, highlightthickness=0)
canvas.pack()

tk.update()


paddle1 = Paddle1(canvas,'white')
paddle = Paddle(canvas,'white')


ball = Ball(canvas, paddle, paddle1, 'white')

while 1:
    # if canvas('<space>'):
    ball.draw()  #공 인스턴스의 draw메소드 실행(공이 화면에 부딪혀도 나가지 않게)
    paddle.draw() #패들을 키보드 방향키로 조정하면서 패들이 화면바깥으로 나가지 않게 실행
    paddle1.draw()
    tk.update_idletasks()  #tkinter에게 계속 화면을 그리라고 명령
    tk.update()    #구현된 내용을 반영
    time.sleep(0.02)  #게임을 사람이 보기 편하게 100분의 2초씩 잠들어라