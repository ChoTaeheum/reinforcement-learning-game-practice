# 오목 게임
import random
import csv

EMPTY = 0  # 비어있는 칸은 0으로
DRAW = 3  # 비긴 경우는 3으로

# 9x9 오목판 만들기

BOARD_FORMAT = "------0--------1--------2--------3------" \
               "--4--------5--------6--------7--------8------\n0| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n1| {9} | {10} | {11} | {12} | {13} | {14} | {15} | {16} | {17} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n2| {18} | {19} | {20} | {21} | {22} | {23} | {24} | {25} | {26} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n3| {27} | {28} | {29} | {30} | {31} | {32} | {33} | {34} | {35} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n4| {36} | {37} | {38} | {39} | {40} | {41} | {42} | {43} | {44} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n5| {45} | {46} | {47} | {48} | {49} | {50} | {51} | {52} | {53} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n6| {54} | {55} | {56} | {57} | {58} | {59} | {60} | {61} | {62} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n7| {63} | {64} | {65} | {66} | {67} | {68} | {69} | {70} | {71} |\n|" \
               "----------------------------------------" \
               "--------------------------------------------\n8| {72} | {73} | {74} | {75} | {76} | {77} | {78} | {79} | {80} |\n" \
               "----------------------------------------" \
               "---------------------------------------------"
# 오목판 관련 클래스
class board():
    @staticmethod
    def emptyboard(): # 초기 바둑판 좌표값
        empty_board = [[EMPTY for i in range(9)] for i in range(9)]
        return empty_board  # [ [EMPTY,EMPTY,EMPTY... EMPTY 총 9개], [EMPTY,EMPTY,EMPTY... EMPTY 총 9개], ...]
        # [ [EMPTY x 9] x 9 ]  로 이뤄진 리스트 만들기. 즉 모든 값이 EMPTY 인 9x9의 리스트 생성

    @staticmethod
    def printboard(state):  # 바둑판에 돌 놓기
        Names = ['      ', '  ●  ', '  ○  '] # Names[0] -> 비어있는 경우 ' ', Names[1] -> Player1 의 돌은 흑돌, Names[2] -> Player2 의 돌은 백돌
        ball = []  # 임의의 리스트 ball 을 만들어서
        for i in range(9):
            for j in range(9):
                ball.append(Names[state[i][j]].center(3))  # 바둑판 좌표 state[i][j] 의 값이 1이면 Names[1] -> 흑돌을 리스트에 입력
        print(BOARD_FORMAT.format(*ball))  # 처음에 만든 BOARD_FORMAT 바둑판에 돌 놓기



# 머신러닝 관련 클래스
class Agent(object):
    def __init__(self, player, verbose=False, lossval=0, learning=True, epsilon=0.1, prevloc=None, loc=None ):
        self.values = {}          # 게임결과인 가중치를 저장하는 딕셔너리
        self.player = player      # 플레이어명
        self.verbose = verbose    # 사람과 게임할 때 가중치를 바둑판에 출력해주는 변수. True 시 출력
        self.lossval = lossval    # 게임 졌을 때의 가중치로, 일반적으로 -1 값을 줌
        self.learning = learning  # 가중치를 갱신하여 학습할지 결정하는 변수. True 시 학습
        self.epsilon = epsilon    # 가중치와 상관없이 랜덤으로 수를 두는 비율. default 값은 0.1(10%)
        self.alpha = 0.99         # 게임 종료 시, 이전까지 둔 수들의 가중치를 역산할 때 사용하는 값.
                                  # (이겼을 때 마지막 수의 가중치가 1이면 그 이전 수에는 1 * 0.99, 그 이전 수에는 1 * 0.99^2 만큼 가중치 반영)
        self.efficiencyrate = 0.8 # 다음 수를 둘 때, 지금까지 상대편과 자신이 둔 수 근처에 수를 두는 비율
                                  # 이걸 고려하지 않고 다음 수를 아예 무작위로 두게 한다면 게임 승패에 관련이 적은 수들이 많이 나와서 효율성이 떨어지므로
                                  # efficiencyrate를 이용해 최대한 승패와 관련된 수를 두도록(지금까지 둔 수 근처에 두도록) 해줌.
                                  # 이와 관련된 메소드는 greedy 메소드
        self.prevstate = []       # 한 게임을 치르며 지금까지 뒀던 수들을 저장하는 리스트. 역산하여 가중치 줄 때 사용
        self.prevscore = 0        # 가중치값
        self.prevloc = prevloc    # 지금까지의 가중치값이 저장된 파일의 위치정보로, 누적된 가중치값을 사용하고자 할 때 입력
        self.loc = loc            # 학습 후 가중치값을 저장할 파일의 위치정보
        if self.prevloc is not None: # 누적된 가중치값을 사용하고자 한다면,
            self.readCSV()           # readCSV() 메소드를 실행해준다! 는 의미. 사용하지 않을 때는 prevloc == None으로 설정

    def readCSV(self):            # 파일로 저장된 가중치값을 읽어들일 때 사용하는 메소드
            try :
                file = open(self.prevloc, 'r')  # 파일은 __main__절에서 다음 형식으로 저장됨.
                                                # 컬럼1 : 플레이어 정보(1or2)
                                                # 컬럼2 : 오목판의 상태(state) 정보
                                                # 컬럼3 : 상태 별 가중치값

                values_list = csv.reader(file)
                for value in values_list:
                    if int(value[0]) == self.player: # 파일 플레이어 정보가 해당 플레이어와 일치하면 다음 값들을 저장해라!라는 의미
                        try:
                            self.values[tuple(eval(value[1]))] = round(float(value[2]),5)

                            # self.values[tuple(eval‎(value[1]))] = round(float(value[2]),5)
                                                     # 가중치 딕셔너리( self.values ) 에
                                                     # 오목판 상태 정보를 key로, 가중치값을 value로 저장
                        except ValueError:
                            continue
            except FileNotFoundError:
                values = {}

    def saveCSV(self, loc, values):
        if not loc is None:
            for key in values:
                if self.values[key] != 0.5:
                    Fn = (loc)
                    w = csv.writer(open(Fn, 'a'), delimiter=',', lineterminator='\n')
                    w.writerow([self.player, key, self.values[key]])


    def Action(self, state):    # 인공지능 플레이어의 행동 기준을 설정한 메소드
        r = random.random()     # 0~1 사이의 값 랜덤 출력
        rr = random.random()    #     "         "
        if r < self.epsilon:    # 가중치와 무관하게 랜덤하게 수를 둘 비율(self.epsilon)보다 작은 값이 출력된 경우
                                # 즉, epsilon이 0.1일 때는 10%의 확률로 랜덤하게 수를 두라는 실행절
            move = self.random(state)
            self.log('>>>>>>> Exploratory action: ' + str(move))
        else:                   # 그렇지 않을 경우 정상적으로 가장 좋은 가중치값을 고려하여 수를 두라는 실행절
            if rr <= self.efficiencyrate:   # 정상적으로 둘 경우에도 일정확률로 효율적인 수(상대와 내가 둔 수에 인접한 수)를 두라는 실행절
                move = self.greedy(state,efficiency=True) # move는 플레이어가 둔 수를 뜻함.
                                                          # self.greedy()는 가장 좋은 가중치값을 판단해서 수를 두게 해주는 메소드
                self.log('>>>>>>> Best action(eff): ' + str(move))
            else:                           # 정상적으로 두면서 효율적인 수 뿐 아니라 모든 수를 대상으로 가중치값을 고려하여 수를 두라는 실행절
                move = self.greedy(state)
                self.log('>>>>>>> Best action(non eff): ' + str(move)) # self.log 메소드는 디버깅용, 출력용 메소드로 크게 중요x
        state[move[0]][move[1]] = self.player  # move 는 튜플 변수로, 바둑판의 정보가 담겨 있음. 예) move = (0,0) --> 바둑판 1행 1열 정보
        self.prevstate.insert(0,self.statetuple(state)) # 수를 결정한 다음에는 지금까지 뒀던 수를 저장한 prevstate 에 저장.
                                                        # 이때 최근 수를 뒤가 아닌 앞에 붙여넣음. (최근 수일수록 리스트의 왼쪽에 위치)
        self.prevscore = self.lookup(state)             # self.lookup() 메소드는 해당 오목판 상태(state)의 가중치를 출력하는 메소드로
                                                        # 지금 둔 수의 가중치를 prevscore에 저장해줌
        state[move[0]][move[1]] = EMPTY                 # 다시 상태 변수(state) 초기화하는 이유 : play()함수에서 입력해주므로
                                                        # 그렇다면 왜 여기서 상태 변수에 값을 굳이 넣어줬다가 초기화했는가? prevstate, prevscore 값을 입력하기 위해
        return move                                     # self.action() 메소드는 이번 턴에 둘 수의 좌표(move)를 출력

    def random(self, state):                       # 수를 랜덤하게 둘 때 쓰는 메소드
        available = []
        for i in range(9):
            for j in range(9):
                if state[i][j] == EMPTY:
                    available.append((i, j))
        return random.choice(available)

    def greedy(self, state, efficiency = False):   # 수를 정상적으로 가중치를 고려하여 둘 때 쓰는 메소드
                                                   # 크게 근접한 수를 두는지(efficiency=True) 아닌지로 나뉘어짐
        maxval = None                              # 이번턴에 둘 수 있는 수들의 가중치 중 최대값
        maxmove = None                             # 이번 턴에서 최대 가중치를 얻게 해주는 최적의 수 좌표(move)
        maxdic = {}                                # 이번 턴에 둘 수 있는 모든 수들의 좌표(key)와 가중치(value)를 저장하는 딕셔너리
        maxlist = []                               # 최대 가중치 값을 얻게 하는 수가 여러개일 때, 이들을 저장하는 리스트
                                                   # 다수의 최적의 수 좌표에서 random 하게 maxmove를 선택하기 위해 필요
        efficiencylist = []                        # efficiency=True 일 때 사용하는 리스트

        if efficiency == False:                    # 인접한 수 외에도 전체 수를 대상으로 최적값을 선택할 때의 실행절
            for i in range(9):
                for j in range(9):
                    if state[i][j] == EMPTY:       # 아직 아무도 안 뒀다면(내가 이번 턴에 둘 수 있는 수라면)
                        state[i][j] = self.player  # 해당 좌표에 수를 뒀다고 가정할때,(미리 한번 값을 입력해보고)
                        val = self.lookup(state)   # 가중치값을 self.lookup 메소드로 불러와서 val 에 저장하고
                        state[i][j] = EMPTY        # 다시 입력한 값을 지워버린다
                        maxdic[(i,j)] = val        # 그리고 maxdic 딕셔너리에 해당 좌표를 key 로 삼고 가중치를 value 로 삼아서 저장

        elif efficiency == True:                   # 지금까지 뒀던 수들에 인접한 수에만 둬서 효율적으로 최적값을 선택할 때의 실행절
            emptylist=[]
            for i in range(9):
                for j in range(9):
                    emptylist.append([i,j])          # emptylist 에 모든 수들의 좌표를 저장
                    if state[i][j] != EMPTY:         # 비어있지 않다면(지금까지 뒀던 수들의 좌표인 경우)
                        efficiencylist.append([i,j]) # efficiencylist 에 추가해둔다.
            if efficiencylist == []:                 # 만약 efficiencylist가 비었다면(지금까지 둔 수들이 없는 경우, 게임 시작 후 첫수를 두는 경우)
                efficiencylist = emptylist           # 모든 수들이 저장된 emptylist를 efficiecylist로 삼는다.(즉 첫 수를 둘 때는 모든 수를 고려한다)
            for efficiencyidx in efficiencylist:
                for i in range(-1, 2, 1):            # range(-1,2,1) 은 지금까지 뒀던 수의 좌표의 행과 열에 각각 -1 만큼, 0만큼, 1만큼 더한 경우
                    for j in range(-1,2,1):          # 즉, 지금까지 뒀던 수를 둘러싼 인접해 있는 수들의 좌표를 표현하기 위해 사용함
                        try:                         # state[0 - 1][1 - 2] 와 같이 인덱스 범위가 초과한 경우 그냥 넘어가도록 함
                            if state[efficiencyidx[0]+i][efficiencyidx[1]+j] == EMPTY:           # 인접한 수가 비어 있으면
                                state[efficiencyidx[0] + i][efficiencyidx[1] + j] = self.player  # 미리 한번 뒀다고 가정하고(시뮬레이션)
                                val = self.lookup(state)                                         # 그때의 가중치값을 val 에 저장해본다.
                                state[efficiencyidx[0] + i][efficiencyidx[1] + j] = EMPTY        # 그리고 다시 초기화한다
                                maxdic[(efficiencyidx[0] + i,efficiencyidx[1] + j)] = val        # maxdic 에 좌표를 key로 가중치값을 value로 저장
                        except IndexError:
                            continue

        for key in maxdic:                           # maxdic 의 키를 모두 뽑아내서
            if maxdic[key] == max(maxdic.values()):  # 해당 키의 가중치 값이 최대 가중치 값인 경우
                maxlist.append(key)                  # 해당 키(최대 가중치를 얻게 해주는 최적의 수의 좌표)를 maxlist에 저장
        maxmove = random.choice(maxlist)             # 최적의 수가 다수라면 그중 랜덤으로 이번 턴의 maxmove 값을 선택
        maxval = max(maxdic.values())                # 그리고 이떄의 최대 가중치를 maxval 로 저장

        self.backup(maxval)                          # self.backup() 메소드는 현재의 가중치를 역산하여 지금까지 뒀던 수들의 가중치값을 갱신해주는 메소드
        return maxmove                               # self.backup() 메소드로 가중치값들을 한번 갱신해준 다음, 최적의 수의 좌표(maxmove)를 출력

    def backup(self, nextval):                       # 지금 둔 수의 가중치값을 역산하여 이전까지 둔 수의 가중치값을 갱신해주는 메소드
        cnt=0
        for key in self.prevstate:                   # 지금까지 둔 수들의 좌표(prevstate)를 불러내서
            if self.prevstate != None and self.learning: # 지금까지 둔 수가 있고, 학습 중이라면
                cnt += 1
                self.values[key] += round((self.alpha ** cnt) * (nextval - self.prevscore),5) # 이렇게 가중치값들을 갱신

    def lookup(self, state):                         # 해당 좌표의 가중치값을 출력하는 메소드
        key = self.statetuple(state)
        if not key in self.values:                   # 만약 해당 좌표가 values딕셔너리에 없다면
            self.add(key)                            # 좌표를 딕셔너리에 저장해주면 되지
        return self.values[key]

    def add(self, state):                            # 좌표가 values 딕셔너리에 없는 경우 좌표와 값을 저장해주는 메소드
        winner = game.gameover(state)
        tup = self.statetuple(state)
        self.values[tup] = self.winnerval(winner)

    def winnerval(self, winner):                     # 게임 종료시 보상값을 설정한 메소드
        if winner == self.player:                    # 이기면 1점
            return 1
        elif winner == EMPTY:                        # 아직 경기 안 끝났을 때는 0.5점
            return 0.5
        elif winner == DRAW:                         # 비겼을 때는 0점
            return 0
        else:                                        # 지면 self.lossval점. default 값은 -1점
            return self.lossval


    def statetuple(self,state):                      # 리스트 타입인 state 변수를 values 딕셔너리의 key의 타입인 튜플 변수로 만들어주는 메소드
        tuple_list = []
        for i in range(9):
            tuple_list.append('tuple(state[{}])'.format(i))
        return (eval(', '.join(tuple_list)))

        # return (eval‎(', '.join(tuple_list)))

    def episode_over(self, winner):                  # 한 경기 끝난 경우의 메소드
        self.backup(self.winnerval(winner))          # 경기의 보상을 역산해주고
        self.prevstate = []                          # 지금까지 뒀던 수와 가중치를 초기화해줌
        self.prevscore = 0

    def log(self, s):                                # 디버깅용. 크게 중요x
        if self.verbose:
            print(s)

# 인간 플레이어 관련 클래스
class human():
    def __init__(self, player):
        self.player = player

    # 돌 놓기
    def Action(self, state):
        board.printboard(state)  # 바둑판 출력
        action = None
        switch_map = {}  # 바둑판 좌표 딕셔너리
        for i in range(9):
            for j in range(9):
                switch_map[10 * i + j] = (i, j)

                # 인풋 받기
        while action not in range(89) or state[switch_map[action][0]][switch_map[action][1]] != EMPTY :
            try:
                action = int(input('Player{}의 차례입니다. '.format(self.player)))
            except ValueError:
                continue

        return switch_map[action]

    # 게임 종료시 출력 문구
    def episode_over(self, winner):
        if winner == DRAW:
            print('무승부입니다.')
        else:
            print('승자는 Player{} 입니다.'.format(winner))

# 게임 진행 및 종료 관련 클래스
class game():
    @staticmethod
    def play(p1, p2):  # 게임 진행
        state = board.emptyboard()
        for i in range(81):
            if i % 2 == 0:
                move = p1.Action(state)
            else:
                move = p2.Action(state)
            state[move[0]][move[1]] = i % 2 + 1
            winner = game.gameover(state)
            if winner != EMPTY:
                board.printboard(state)
                return winner

    @staticmethod
    def gameover(state):  # 게임이 종료되는 조건 함수 생성
        for i in range(9):
            for j in range(9):
                try:
                    # 한쪽이 이겨서 게임 종료되는 경우

                    # 가로로 다섯칸 모두 1인 경우(player1의 흑돌이 가로로 연속 다섯칸에 놓인 경우)
                    if state[i][j] * state[i][j + 1] * state[i][j + 2] * state[i][j + 3] * state[i][j + 4] == 1:
                        return 1
                        # 가로로 다섯칸 모두 2인 경우(player2의 백돌이 가로로 연속 다섯칸에 놓인 경우)
                    if state[i][j] * state[i][j + 1] * state[i][j + 2] * state[i][j + 3] * state[i][
                                j + 4] == 32:
                        return 2
                        # 세로로 다섯칸 모두 1인 경우(player1의 흑돌이 세로로 연속 다섯칸에 놓인 경우)
                    if state[j][i] * state[j + 1][i] * state[j + 2][i] * state[j + 3][i] * state[j + 4][i] == 1:
                        return 1
                        # 세로로 다섯칸 모두 2인 경우(player2의 백돌이 가로로 연속 다섯칸에 놓인 경우)
                    if state[j][i] * state[j + 1][i] * state[j + 2][i] * state[j + 3][i] * state[j + 4][
                        i] == 32:
                        return 2
                        # 대각선으로 다섯칸 모두 1인 경우(player1의 흑돌이 대각선으로 연속 다섯칸에 놓인 경우)
                    if state[i][j] * state[i + 1][j + 1] * state[i + 2][j + 2] * state[i + 3][j + 3] * \
                            state[i + 4][
                                        j + 4] == 1:
                        return 1
                    if state[i][j + 4] * state[i + 1][j + 3] * state[i + 2][j + 2] * state[i + 3][j + 1] * \
                            state[i + 4][
                                j] == 1:
                        return 1
                        # 대각선으로 다섯칸 모두 2인 경우(player2의 백돌이 대각선으로 연속 다섯칸에 놓인 경우)
                    if state[i][j] * state[i + 1][j + 1] * state[i + 2][j + 2] * state[i + 3][j + 3] * \
                            state[i + 4][
                                        j + 4] == 32:
                        return 2
                    if state[i][j + 4] * state[i + 1][j + 3] * state[i + 2][j + 2] * state[i + 3][j + 1] * \
                            state[i + 4][
                                j] == 32:
                        return 2

                except IndexError:  # range(9)로 인덱스 범위 넘어가는 경우 continue 로 예외처리하여 에러 안 뜨게 함
                    continue

                    # 한쪽이 이겨서 게임이 종료된 경우가 아니며, 빈칸이 존재하는 경우 계속 진행
        for i in range(9):
            for j in range(9):
                if state[i][j] == EMPTY:
                    return EMPTY
                    # 한쪽이 이겨서 게임이 종료된 경우가 아니며, 빈칸도 없는 경우 비김
        return DRAW

if __name__ == '__main__':

    # 파일 저장, 불러오기 input 실행절
    if input('Save 하시겠습니까?(True or False) ').upper() == 'TRUE':
        input_loc = input('저장위치를 입력해주세요(예 : C:\OMOK.csv or None 입력) ')
    else :
        input_loc = None
    input_prevloc = input('참고할 파일 위치를 입력해주세요(예: C:\OMOK.csv or None 입력) ')
    p1 = Agent(1, lossval=-1, prevloc= input_prevloc, loc = input_loc)
    p2 = Agent(2, lossval=-1, prevloc= input_prevloc, loc = input_loc)

    # 인공지능 간의 대결.
    for i in range(5):
        if i % 10 == 0:
            print('Game: {0}'.format(i))

        winner = game.play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)

    # 인공지능 간의 대결 후 좌표와 가중치 값을 저장해줌.
    # 이때 저장된 좌표와 가중치값 을 바탕으로 (values 딕셔너리를 이용하여) 이후 사람과 대결함
    p1.saveCSV(p1.loc, p1.values)
    p2.saveCSV(p2.loc, p2.values)

    # 사람과 인공지능 대결
    while True:
        p2.verbose = True
        p2.epsilon = 0
        p1 = human(1)
        winner = game.play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)