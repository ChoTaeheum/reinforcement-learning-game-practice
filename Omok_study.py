EMPTY = 0  #비어있는 칸 0으로
DRAW = 3   #비긴 결과는 3으로

#9*9 바둑판 만들기

BOARD_FORMAT = \
"|----1----2----3----4----5----6----7----8----9----|\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"1|---{0}----{1}----{2}----{3}----{4}----{5}----{6}----{7}----{8}---|1\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"2|---{9}----{10}----{11}----{12}----{13}----{14}----{15}----{16}----{17}---|2\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"3|---{18}----{19}----{20}----{21}----{22}----{23}----{24}----{25}----{26}---|3\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"4|---{27}----{28}----{29}----{30}----{31}----{32}----{33}----{34}----{35}---|4\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"5|---{36}----{37}----{38}----{39}----{40}----{41}----{42}----{43}----{44}---|5\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"6|---{45}----{46}----{47}----{48}----{49}----{50}----{51}----{52}----{53}---|6\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"7|---{54}----{55}----{56}----{57}----{58}----{59}----{60}----{61}----{62}---|7\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"8|---{63}----{64}----{65}----{66}----{67}----{68}----{69}----{70}----{71}---|8\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"9|---{72}----{73}----{74}----{75}----{76}----{77}----{78}----{79}----{80}---|9\n"\
"|    |    |    |    |    |    |    |    |    |    |\n"\
"|----1----2----3----4----5----6----7----8----9----|"
#바둑판은 0부터 시작

NAMES = [' ', 'O', 'X']  #바둑돌 파이참에서는 ●이 2byte라서 칸이 안맞는다.

def printboard(state):
    stone = []  #바둑판에 돌의 위치를 표시하기 위한 리스트변수
    for i in range(9):       #바둑판 가로좌표
        for j in range(9):   #바둑판 세로좌표
            stone.append(NAMES[state[i][j]])
            #Action에서 받은 바둑돌(1,2)을 NAMES에서 돌(O,X)로 변환시켜서 stone에 넣는 과정입니다.
    print(BOARD_FORMAT.format(*stone))
    #stone리스트에 들어있는 반복자들을 BOARD_FORMAT에 넣어서 출력해라

def emptyboard():
    empty_board = [[EMPTY for i in range(9)] for j in range(9)]
    return empty_board
    #emptyboard 함수를 위에서 만든 empty_board 변수로 return하겠다.
###[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, ......]]

#printboard(emptyboard())  #변수로 함수를 사용하여 비어있는 바둑판 출력

class Human():
    def __init__(self, player):
        self.player = player

    def player_action(self, state):
        printboard(state)   #state 어디서 가져오는 건지 아직 모르게씀
        action = None
        switch_map = {}     #바둑판 좌표 딕셔너리
        for i in range(1, 10):
            for j in range(1, 10):
                switch_map[10 * i + j] = (i, j)
# #####@@@@switch_map에 어떻게 key와 values가 담길까??#########
# # switch_map = {}
# # for i in range(1, 10):
# #     for j in range(1, 10):
# #         switch_map[10 * i + j] = (i, j)
# # print(switch_map)
# #{11: (1, 1), 12: (1, 2), 13: (1, 3), 14: (1, 4), ....}
# #이렇게 담는 거 좀 신기함 할당 연산자(=) 이렇게 사용해서 콜론(:)으로 사용됨
        while action not in range(11, 100) or state[switch_map[action][0] - 1][switch_map[action][1] - 1] != EMPTY:
        #input되는 숫자가 11에서 100사이가 아니거나 공백으로 입력되면 계속해서 물어봐라
        ####or 뒷부분 이해 안돼
                try:
                    action = int(input('player{}의 차례입니다.'.format(self.player)))
                    #여기서 action에 변수를 받아서 while문에서 필터링해서  들어간다.
                except ValueError:
                    continue  #valueerror가 떠도 그냥 계속 while loop돌려라!!
        return switch_map[action]
    #action에서 매개변수로 받아서 그에 대응하는 switch_map값 (한개) 리턴!
    def episode_over(self, winner):  #winner 값 받아서 메세지 출력
        if winner == DRAW:
            print('무승부입니다. ')
        else:
            print('player{}의 승리입니다.'.format(winner))

def play(p1, p2):
    state = emptyboard()
    for i in range(81): # 9*9 = 81
        if i % 2 == 0:
            move = p1.player_action(state)
        else:
            move = p2.player_action(state)
        state[move[0] - 1][move[1] - 1] = i % 2 + 1
        #여기에서 state(위에서 emptyboard로 선언해준..)에 아까 input받은 action값을 넣어준다.
        winner = gameover(state)
        if winner != EMPTY:      #winner가 존재하면
            printboard(state)   #emptyboard받아서 input해준놈이 state!!
            return winner
    return winner   #어차피 걍 winner 반환

def gameover(state):  #변수로 반복자를 받음!@!!
    for i in range(9):
        for j in range(9):
            try:
                #한쪽이 이겨서 게임이 종료되는 경우

                #가로, 세로로 5칸이 되어서 이기는 경우
                if state[i][j] * state[i][j+1] * state[i][j+2] * state[i][j+3] * state[i][j+4] == 1:
                    return 1
                if state[i][j] * state[i][j+1] * state[i][j+2] * state[i][j+3] * state[i][j+4] == 32:
                    return 2
                if state[i][j] * state[i+1][j] * state[i+2][j] * state[i+3][j] * state[i+4][j] == 1:
                    return 1
                if state[i][j] * state[i+1][j] * state[i+2][j] * state[i+3][j] * state[i+4][j] == 32:
                    return 2

                #대각선으로 5칸이 차서 이기는 경우
                if state[i][j] * state[i+1][j+1] * state[i+2][j+2] * state[i+3][j+3] * state[i+4][j+4] == 1:
                    return 1
                if state[i][j] * state[i+1][j+1] * state[i+2][j+2] * state[i+3][j+3] * state[i+4][j+4] == 32:
                    return 2

                if state[i][j] * state[i+1][j-1] * state[i+2][j-2] * state[i+3][j-3] * state[i+4][j-4] == 1:
                    return 1
                if state[i][j] * state[i+1][j-1] * state[i+2][j-2] * state[i+3][j-3] * state[i+4][j-4] == 32:
                    return 2
            except IndexError:   #range를 넘어서서 입력받을 경우 continue로 받아서 에러코드 뜨지 않게
                continue         #근데 이거 왜 받아야하냐면 위에 while에서 인덱스 넘어가지 않는 경우에 실행하라고 했지 넘어가는 경우 어떻게 해주라는 예외처리는 없었음

    for i in range(9):     #여기서 한번 더 loop
        for j in range(9):
            if state[i][j] == EMPTY:
                return EMPTY    #하나라도 EMPTY있으면 EMPTY반환????

    return DRAW ##위에서 아무 경우도 안걸리면 DRAW 반환!!!!!!!!!!!!!!!!

if __name__ == '__main__':
    p1 = Human(1)
    p2 = Human(2)
    while True:
        winner = play(p1, p2)   #여기서 p1, p2 돌아가면서 바꿔진다.
        p1.episode_over(winner)
        #메세지 출력인데 1, 2, 3에 해당하지 않아서 continue로 gameover loop빠져 나오면 아무것도
        #출력하지 않고 다시 while True 돈다.
        if winner != '':
            break
