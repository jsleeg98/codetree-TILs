import sys
import heapq

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline
INF = sys.maxsize

class Santa:
    def __init__(self):
        self.r = 0
        self.c = 0
        self.t = 0
        self.score = 0
        self.s = True

dir_r = [(-1, -1), (-1, 0), (-1, 1),
         (0, -1), (0, 1),
         (1, -1), (1, 0), (1, 1)]

def move_r(T):
    global Rr, Rc, tmp_board, cnt_survive
    min_dist = INF
    li_can = []
    # 탈락하지 않은 산타 리스트에 추가
    for i in range(1, P + 1):
        if santas[i].s:
            # 루돌프와 거리 측정
            dist = (santas[i].r - Rr) * (santas[i].r - Rr) + (santas[i].c - Rc) * (santas[i].c - Rc)
            if dist < min_dist:
                min_dist = dist
                li_can = [(dist, -santas[i].r, -santas[i].c, i)]
            elif dist == min_dist:
                li_can.append((dist, -santas[i].r, -santas[i].c, i))

    # 산타 선정
    heapq.heapify(li_can)
    tmp_santa = li_can[0]

    min_dist = INF
    Nr, Nc = 0, 0
    dir = 0
    # 방향 선택
    for i in range(8):
        nr = Rr + dir_r[i][0]
        nc = Rc + dir_r[i][1]
        if nr < 1 or N < nr or nc < 1 or N < nc:
            continue
        dist = (nr - (tmp_santa[1] * -1)) * (nr - (tmp_santa[1] * -1)) + (nc - (tmp_santa[2] * -1)) * (nc - (tmp_santa[2] * -1))
        if dist < min_dist:
            min_dist = dist
            Nr = nr
            Nc = nc
            dir = i

    # 루돌프 돌진
    Rr = Nr
    Rc = Nc
    board = [[0 for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]  # 보드
    # 보드에 산타 위치 표시
    for i in range(1, P + 1):
        if santas[i].s:
            board[santas[i].r][santas[i].c] = i

    tmp_board = [[0 for _ in range(N + 1)] for _ in range(N + 1)]  # 임시 보드 초기화
    if board[Rr][Rc] != 0:  # 산타와 충돌한 경우
        id = board[Rr][Rc]  # 산타 번호
        santas[id].score += C  # 산타 점수 추가
        SNr = santas[id].r + dir_r[dir][0] * C
        SNc = santas[id].c + dir_r[dir][1] * C
        santas[id].r = SNr
        santas[id].c = SNc
        santas[id].t = T + 2  # 기절
        if SNr < 1 or N < SNr or SNc < 1 or N < SNc:  # 보드를 벗어난 경우
            santas[id].s = False  # 탈락 처리
            cnt_survive -= 1
        elif board[SNr][SNc] != 0:  # 다른 산타와 충돌한 경우
            interaction_santa_ro(board[SNr][SNc], dir)
        else:  # 비어 있는 경우
            pass


def interaction_santa_ro(santa_num, dir):
    global tmp_board, cnt_survive
    SNr = santas[santa_num].r + dir_r[dir][0]
    SNc = santas[santa_num].c + dir_r[dir][1]
    santas[santa_num].r = SNr
    santas[santa_num].c = SNc
    if SNr < 1 or N < SNr or SNc < 1 or N < SNc:  # 보드를 벗어난 경우
        santas[santa_num].s = False  # 탈락 처리
        cnt_survive -= 1
    elif board[SNr][SNc] != 0:  # 다른 산타와 충돌한 경우
        tmp_board[SNr][SNc] = santa_num
        interaction_santa_ro(board[SNr][SNc], dir)
    else:  # 산타가 없는 경우
        tmp_board[SNr][SNc] = santa_num


dir_s = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def interaction_santa(santa_num, dir):
    global tmp_board, cnt_survive
    SNr = santas[santa_num].r + dir_s[dir][0]
    SNc = santas[santa_num].c + dir_s[dir][1]
    santas[santa_num].r = SNr
    santas[santa_num].c = SNc
    if SNr < 1 or N < SNr or SNc < 1 or N < SNc:  # 보드를 벗어난 경우
        santas[santa_num].s = False  # 탈락 처리
        cnt_survive -= 1
    elif board[SNr][SNc] != 0:  # 다른 산타와 충돌한 경우
        before_num = board[SNr][SNc]
        board[SNr][SNc] = santa_num
        interaction_santa(before_num, dir)
    else:  # 산타가 없는 경우
        tmp_board[SNr][SNc] = santa_num


def move_s(T):
    global tmp_board, cnt_survive

    board = [[0 for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]  # 보드
    # 보드에 산타 위치 표시
    for i in range(1, P + 1):
        if santas[i].s:
            board[santas[i].r][santas[i].c] = i

    tmp_board = [[0 for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]  # 보드
    for i in range(1, P + 1):
        if santas[i].s:
            if santas[i].t <= T:
                Fr, Fc = 0, 0  # 최종 움직일 위치
                dir = 0  # 최종 움직일 방향
                min_dist = (santas[i].r - Rr) * (santas[i].r - Rr) + (santas[i].c - Rc) * (santas[i].c - Rc)
                for d in range(4):
                    Nr = santas[i].r + dir_s[d][0]
                    Nc = santas[i].c + dir_s[d][1]
                    if Nr < 1 or N < Nr or Nc < 1 or N < Nc:  # 맵 벗어나는 경우 패스
                        continue
                    if board[Nr][Nc] != 0:  # 산타가 있는 경우 패스
                        continue
                    dist = (Nr - Rr) * (Nr - Rr) + (Nc - Rc) * (Nc - Rc)
                    if dist < min_dist:
                        min_dist = dist
                        Fr = Nr
                        Fc = Nc
                        dir = d
                if Fr == 0 and Fc == 0:  # 가까워지지 않는 경우 패스
                    continue
                # 움직이는 경우 현재 위치에서 삭제
                board[santas[i].r][santas[i].c] = 0
                santas[i].r = Fr
                santas[i].c = Fc
                # 루돌프가 있는 경우
                if Fr == Rr and Fc == Rc:
                    santas[i].score += D  # 산타 점수 D 얻음
                    santas[i].t = T + 2
                    # 반대 방향으로 D 칸 밀려남
                    op_dir = (dir + 2) % 4
                    SNr = santas[i].r + dir_s[op_dir][0] * D
                    SNc = santas[i].c + dir_s[op_dir][1] * D
                    santas[i].r = SNr
                    santas[i].c = SNc
                    # 충돌 후
                    if SNr < 1 or N < SNr or SNc < 1 or N < SNc:  # 보드를 벗어난 경우
                        santas[i].s = False  # 탈락 처리
                        cnt_survive -= 1
                    elif board[SNr][SNc] != 0:  # 다른 산타와 충돌한 경우
                        before_num = board[SNr][SNc]
                        board[SNr][SNc] = i
                        interaction_santa(before_num, op_dir)
                    else:  # 비어 있는 경우
                        board[SNr][SNc] = i
                else:  # 비어있는 경우
                    board[Fr][Fc] = i

def add_score():
    global santas

    for i in range(1, P + 1):
        if santas[i].s:
            santas[i].score += 1

def print_santa_ro(santas):
    m = [[0 for _ in range(N + 1)] for _ in range(N + 1)]

    for i in range(1, P + 1):
        if santas[i].s:
            m[santas[i].r][santas[i].c] = i

    m[Rr][Rc] = -1

    for r in range(1, N + 1):
        for c in range(1, N + 1):
            print(m[r][c], end=' ')
        print()
    print('-' * 20)


MAX_N = 50
MAX_P = 30

tmp_board = [[0 for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]  # 보드
board = [[0 for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]  # 보드
# board[Rr][Rc] = 1  # 루돌프 위치 표시
santas = [Santa() for _ in range(MAX_P + 1)]  # 산타 리스트


N, M, P, C, D = map(int, input().split())
Rr, Rc = map(int, input().split())
for _ in range(P):
    num, r, c = map(int, input().split())
    santas[num].r = r
    santas[num].c = c

cnt_survive = P

# print_santa_ro(santas)
for T in range(1, M + 1):
    # print(T)
    move_r(T)
    # print_santa_ro(santas)
    move_s(T)
    # print_santa_ro(santas)
    # print('=' * 20)
    add_score()
    if cnt_survive == 0:
        break

for i in range(1, P + 1):
    print(santas[i].score, end=' ')