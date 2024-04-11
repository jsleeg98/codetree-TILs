MAX_N = 99
runner_board = [[[] for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]
runner_r = [0 for _ in range(MAX_N ** 2)]
runner_c = [0 for _ in range(MAX_N ** 2)]
runner_d = [0 for _ in range(MAX_N ** 2)]
runner_state = [0 for _ in range(MAX_N ** 2)]
tree_board = [[0 for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]
mom_r = 0
mom_c = 0
mom_d = 0

dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
n = 0
limit = []
rotate_dir = 1
limit_i = 0
mom_cnt = 0
score = 0

def inRange(r, c):
    if 1 <= r <= n and 1 <= c <= n:
        return True
    else:
        return False

def move_runner():
    global runner_r, runner_c, runner_d
    for i in range(1, m + 1):
        if runner_state[i] == 0:  # 죽은 도망자 패스
            continue
        # 거리 측정
        dist = abs(runner_r[i] - mom_r) + abs(runner_c[i] - mom_c)
        # 이동
        if dist <= 3:
            cr = runner_r[i]
            cc = runner_c[i]
            nr = cr + dir[runner_d[i]][0]
            nc = cc + dir[runner_d[i]][1]
            # 벽 바깥인 경우
            if not inRange(nr, nc):
                # 방향 변경
                runner_d[i] = (runner_d[i] + 2) % 4
                # 새로운 위치 수정
                nr = cr + dir[runner_d[i]][0]
                nc = cc + dir[runner_d[i]][1]
                # 돌았는 데 술래가 있는 곳인 경우
                if nr == mom_r and nc == mom_c:
                    continue
                else:  # 돌았는데 술래가 없는 곳인 경우
                    # 도망자 이동
                    runner_r[i] = nr
                    runner_c[i] = nc
            else:  # 격자 내부 인경우
                if nr == mom_r and nc == mom_c:  # 술래가 있는 경우
                    continue
                else:  # 술래가 없는 곳인 경우
                    # 도망자 이동
                    runner_r[i] = nr
                    runner_c[i] = nc
def move_mom():
    global rotate_dir, limit_i, mom_cnt, mom_d, mom_r, mom_c

    nr = mom_r + dir[mom_d][0]
    nc = mom_c + dir[mom_d][1]
    mom_cnt += 1
    if mom_cnt == limit[limit_i]:
        mom_cnt = 0
        limit_i += rotate_dir
        if limit_i == 2 * n:
            limit_i = 2 * n - 1
            rotate_dir = -1
            mom_d = (mom_d + 2) % 4
        elif limit_i == 0:
            limit_i = 1
            rotate_dir = 1
            mom_d = (mom_d + 2) % 4
        else:
            mom_d = (mom_d + rotate_dir) % 4
    mom_r = nr
    mom_c = nc

def print_mom():
    tmp_board = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    tmp_board[mom_r][mom_c] = 1

    for r in range(1, n + 1):
        for c in range(1, n + 1):
            print(tmp_board[r][c], end=' ')
        print()
    print()

def catch(k):
    global score
    # 도망자 위치 저장
    runner_board = [[[] for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]
    for i in range(1, m + 1):
        if runner_state[i] == 1:
            runner_board[runner_r[i]][runner_c[i]].append(i)
    # 술래 방향 3칸 얻기
    cur_r = mom_r
    cur_c = mom_c
    li_catch = []
    for i in range(0, 3):
        nr = cur_r + dir[mom_d][0] * i
        nc = cur_c + dir[mom_d][1] * i
        if not inRange(nr, nc):  # 격자 밖 종료
            break
        if tree_board[nr][nc] == 1:  # 나무 위치 잡을 수 없음
            continue
        li_catch.append((nr, nc))

    # for r in range(1, n + 1):
    #     for c in range(1, n + 1):
    #         print(runner_board[r][c], end=' ')
    #     print()

    # 볼 수 있는 칸 중 도둑이 있는 지 확인
    for pos in li_catch:
        if len(runner_board[pos[0]][pos[1]]) > 0:
            score += len(runner_board[pos[0]][pos[1]]) * k
            for runner in runner_board[pos[0]][pos[1]]:
                runner_state[runner] = 0  # 잡힘 표시
    # print(mom_r, mom_c, mom_d)

n, m, h, K = map(int, input().split())
for i in range(1, m + 1):
    tmp_r, tmp_c, tmp_d = map(int, input().split())
    runner_r[i] = tmp_r
    runner_c[i] = tmp_c
    runner_d[i] = tmp_d
    runner_state[i] = 1  # 도망자 소환
for i in range(h):
    tmp_r, tmp_c = map(int, input().split())
    tree_board[tmp_r][tmp_c] = 1

mom_r = (n // 2) + 1
mom_c = (n // 2) + 1
mom_d = 0
mom_cnt = 0

score = 0

# limit 초기화
limit = [0]
for i in range(1, n):
    limit.append(i)
    limit.append(i)
limit.append(n - 1)
# print(limit)
# rotate_dir 초기화
rotate_dir = 1

limit_i = 1

for k in range(1, K + 1):
    # 도망자 이동
    move_runner()
    # 술래 이동
    move_mom()
    # 잡기
    catch(k)
    # print_mom()
print(score)