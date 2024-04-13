from collections import deque
import queue

train_length = []
board = []  # 0행 0열 시작
trains = []  # 0번 기차부터 시작
dir = [(0, 1), (-1, 0), (0, -1), (1, 0)]
nxt = [(1, 0), (0, 1), (-1, 0), (0, -1)]
tmp_cnt = 0
nxt_idx = -1
visit = []
train_board = []
sr = 0
sc = 0
total_score = 0


n, m, k = map(int, input().split())



for i in range(n):
    board.append(list(map(int, input().split())))

for i in range(m):
    trains.append(deque())

def inRange(r, c):
    if 0 <= r <= n-1 and 0 <= c <= n-1:
        return True
    else:
        return False

def dfs(train_idx, cr, cc, length, rail):
    global visit
    trains[train_idx].append((cr, cc))
    for i in range(4):
        nr = cr + dir[i][0]
        nc = cc + dir[i][1]
        if not inRange(nr, nc):
            continue
        if visit[nr][nc] == 1:
            continue
        if board[nr][nc] == 2:
            visit[nr][nc] = 1
            dfs(train_idx, nr, nc, length + 1, False)
        elif board[nr][nc] == 3:
            visit[nr][nc] = 1
            dfs(train_idx, nr, nc, length + 1, True)
            train_length.append(length + 1)
        if rail:
            if board[nr][nc] == 4:
                visit[nr][nc] = 1
                dfs(train_idx, nr, nc, length, True)

def update_line():
    global tmp_cnt, nxt_idx, sr, sc
    if tmp_cnt == 0:
        tmp_cnt += 1
        nxt_idx += 1
        nxt_idx = nxt_idx % 4
    else:
        tmp_cnt += 1
        tmp_cnt = tmp_cnt % n
        sr = sr + nxt[nxt_idx][0]
        sc = sc + nxt[nxt_idx][1]

train_idx = 0
for r in range(n):
    for c in range(n):
        if board[r][c] == 1:
            visit = [[0 for _ in range(n)] for _ in range(n)]
            visit[r][c] = 1
            dfs(train_idx, r, c, 1, False)
            train_idx += 1

for _ in range(k):
    # 기차 전진
    for i in range(m):
        tmp = trains[i].pop()
        trains[i].appendleft(tmp)

    # 보드에 기차 번호 표시
    train_board = [[-1 for _ in range(n)] for _ in range(n)]
    for i in range(m):
        for l in range(train_length[i]):
            r, c = trains[i][l]
            train_board[r][c] = i
    
    # for r in range(n):
    #     for c in range(n):
    #         print(train_board[r][c], end=' ')
    #     print()

    # 공 던지기
    attacked_train = {}
    update_line()  # 공 시작 위치 sr, sc
    for i in range(n):
        nr = sr + dir[nxt_idx][0] * i
        nc = sc + dir[nxt_idx][1] * i
        if train_board[nr][nc] != -1:
            if not train_board[nr][nc] in attacked_train.keys():
                attacked_train[train_board[nr][nc]] = (nr, nc)




    # 점수 처리
    for key, value in attacked_train.items():
        # 기차 위치 찾기
        cnt = 1
        for i in range(len(trains[key])):
            if trains[key][i] == value:
                break
            else:
                cnt += 1
        total_score += cnt ** 2

    # 맞은 팀 방향 바꾸기
    for key in attacked_train.keys():
        for i in range(train_length[key]):
            tmp = trains[key].popleft()
            trains[key].append(tmp)
        trains[key].reverse()

print(total_score)