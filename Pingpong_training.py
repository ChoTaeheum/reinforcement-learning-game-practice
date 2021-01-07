from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)  # 공 크기 및 색깔

        self.canvas.move(self.id, 245, 100)  # 공을 캔버스 중앙으로 이동
        starts = [-3, -2, -1, 1, 2, 3]  # 공의 속도를 랜덤으로 구성하기 위해 준비한 리스트
        random.shuffle(starts)  # starts 리스트 중에 숫자를 랜덤으로 골라서
        self.x = starts[0]  # 처음 공이 패들에서 움직일때 왼쪽으로 올라갈지 오른쪽으로 올라갈지 랜덤으로 결정되는 부분
        self.y = -3  # 처음 공이 패들에서 움직일때 위로 올라가는 속도
        self.canvas_height = self.canvas.winfo_height()  # 캔버스의 현재 높이를 반환한다.(공이 화면에서 사라지지 않기위해)
        self.canvas_width = self.canvas.winfo_width()  # 캔버스의 현재 넓이를 반환한다.(공이 화면에서 사라지지 않기위해)
        self.hit_bottom = False

    def hit_paddle(self, pos):  # 패들에 공이 튀기게 하는 함수
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:  # 공이 패들에 내려오기 직전 좌표
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:  # 공이 패들에 닿았을때 좌표
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)  # 공을 움직이게 하는 부분
        # 공이 화면 밖으로 나가지 않게 해준다
        pos = self.canvas.coords(self.id)  # 볼의 현재 좌표를 출력해준다. 공 좌표( 서쪽(0) , 남쪽(1) , 동쪽(2), 북쪽(3) )
        # [ 255,29,270,44]

        if pos[1] <= 0:  # 공의 남쪽이 가리키는 좌표가 0보다 작아진다면 공이 위쪽 화면 밖으로 나가버리므로
            self.y = 3  # 공을 아래로 떨어뜨린다. (공이 위로 올라갈수로 y 의 값이 작아지므로 아래로 내리려면 다시 양수로)
        if pos[3] >= self.canvas_height:  # 공의 북쪽이 가리키는 좌표가 캔버스의 높이보다 더 크다면 화면 아래로 나가버려서
            self.y = -3  # 공을 위로 올린다. (공이 아래로 내려갈수록 y 값이 커지므로 공을 위로 올릴려면 다시 음수로)
        if pos[0] <= 0:  # 공의 서쪽이 가리키는 좌표가 0보다 작으면 공이 화면 왼쪽으로 나가버리므로
            self.x = 3  # 공을 오른쪽으로 돌린다.
        if pos[2] >= self.canvas_width:  # 공의 동쪽이 가리키는 좌표가 공의 넓이보다 크다면 공이 화면 오른쪽으로 나가버림
            self.x = -3  # 공을 왼쪽으로 돌린다.
        if self.hit_paddle(pos) == True:  # 패들 판에 부딪히면 위로 튕겨올라가게
            self.y = -3  # 공을 위로 올린다.


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)  # 패들의 높이와 넓이 그리고 색깔
        self.canvas.move(self.id, 200, 300)  # 패들 사각형을 200,300 에 위치
        self.x = 0  # 패들이 처음 시작할때 움직이지 않게 0으로 설정
        self.canvas_width = self.canvas.winfo_width()  # 캔버스의 넓이를 반환한다. 캔버스 밖으로 패들이 나가지 않도록
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)  # 왼쪽 화살표 키를 '<KeyPress-Left>'  라는 이름로 바인딩
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)  # 오른쪽도 마찬가지로 바인딩한다.

    def draw(self):
        self.canvas.move(self.id, self.x, 0)  # 시작할때 패들이 위아래로 움직이지 않도록 0 으로 설정
        pos = self.canvas.coords(self.id)
        #print(pos)
        if pos[0] <= 0:  # 공의 서쪽이 가리키는 좌표가 0보다 작으면 공이 화면 왼쪽으로 나가버리므로
            self.x = 3  # 패들을 오른쪽으로 움직이게 한다..
        elif pos[2] >= self.canvas_width:  # 공의 동쪽이 캔버스의 넓이 보다 크면 공이 화면 오른쪽으로 나가버리므로
            self.x = -3  # 패들을 왼쪽으로 움직이게 한다.

            # 패들이 화면의 끝에 부딪히면 공처럼 튕기는게 아니라 움직임이 멈춰야한다.
            # 그래서 왼쪽 x 좌표(pos[0]) 가 0 과 같거나 작으면 self.x = 0 처럼 x 변수에 0 을
            # 설정한다.  같은 방법으로 오른쪽 x 좌표(pos[2]) 가 캔버스의 폭과 같거나 크면
            # self.x = 0 처럼 변수에 0 을 설정한다.

    def turn_left(self, evt):  # 패들의 방향을 전환하는 함수
        self.x = -3

    def turn_right(self, evt):
        self.x = 3

    def move(self,x,y):
        self.x = x


tk = Tk()  # tk 를 인스턴스화 한다.
tk.title("Game")  # tk 객체의 title 메소드(함수)로 게임창에 제목을 부여한다.
tk.resizable(0, 0)  # 게임창의 크기는 가로나 세로로 변경될수 없다라고 말하는것이다.
tk.wm_attributes("-topmost", 1)  # 다른 모든 창들 앞에 캔버스를 가진 창이 위치할것을 tkinter 에게 알려준다.

canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
# bg=0,highlightthickness=0 은 캔버스 외곽에 둘러싼
# 외곽선이 없도록 하는것이다. (게임화면이 좀더 좋게)

canvas.pack()  # 앞의 코드에서 전달된 폭과 높이는 매개변수에 따라 크기를 맞추라고 캔버스에에 말해준다.
tk.update()  # tkinter 에게 게임에서의 애니메이션을 위해 자신을 초기화하라고 알려주는것이다.
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')
start = False
# 공을 약간 움직이고 새로운 위치로 화면을 다시 그리며, 잠깐 잠들었다가 다시 시작해 ! "
while 1:
    if ball.hit_bottom == False:
        ball.draw()
        y =300
        starts = [-1,-2,-3,-4,-5,0, 1,2,3,4,5]
        random.shuffle(starts)
        x = starts[0]
        print(x)
        paddle.move(x,y)
        paddle.draw()

    tk.update_idletasks()  # 우리가 창을 닫으라고 할때까지 계속해서 tkinter 에게 화면을 그려라 !
    tk.update()  # tkinter 에게 게임에서의 애니메이션을 위해 자신을 초기화하라고 알려주는것이다.
    time.sleep(0.01)  # 무한 루프중에 100분의 1초마다 잠들어라 !

