import sys
from collections import deque
import heapq
import copy

# sys.stdin = open('input.txt', 'r')
input = sys.stdin.readline
INF = 987654321

class person:
    def __init__(self):
        self.r = 0
        self.c = 0
        self.done = False

dir = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def move_conv():
    global wall, person_done
    next_wall = copy.deepcopy(wall)
    for i in range(1, m + 1):
        if people[i].done == False:
            if people[i].r != 0 and people[i].c != 0:  # 격자에 올려진 경우
                # 네 방향에 대해 각각 도착하기까지 최단거리 측정
                fr = 0
                fc = 0
                f_dist = INF
                # 현재 위치 기록
                cur_r = people[i].r
                cur_c = people[i].c
                # 네 방향에 대해 최단거리로 움직이면서 우선순위에 맞게 선택
                for k in range(4):
                    visit = [[0 for _ in range(n + 1)] for _ in range(n + 1)]  # 방문 맵
                    q = deque()
                    nxt_r = cur_r + dir[k][0]
                    nxt_c = cur_c + dir[k][1]
                    q.append((nxt_r, nxt_c, 1))  # r, c, 1 - 한칸 이동한 것으로 침
                    visit[cur_r][cur_c] = 1  # 원래 위치 방문 처리
                    # 다음 방향이 맵을 벗어난 경우 패스
                    if nxt_r < 1 or n < nxt_r or nxt_c < 1 or n < nxt_c:
                        continue
                    if wall[nxt_r][nxt_c] == 1:
                        continue
                    # 벗어나지 않은 경우
                    visit[nxt_r][nxt_c] = 1  # 다음 위치 방문처리
                    while q:
                        cr, cc, dist = q.popleft()
                        if cr == conv[i][0] and cc == conv[i][1]:  # 편의점에 도착한 경우
                            if dist < f_dist:  # 거리가 짧은 경우만 갱신
                                f_dist = dist
                                fr = nxt_r
                                fc = nxt_c
                            break
                        for j in range(4):
                            nr = cr + dir[j][0]
                            nc = cc + dir[j][1]
                            # 격자 벗어남 패스
                            if nr < 1 or n < nr or nc < 1 or n < nc:
                                continue
                            if wall[nr][nc] == 1:  # 이미 벽인 경우 패스
                                continue
                            if visit[nr][nc] != 0:  # 방문한 경우 패스
                                continue
                            q.append((nr, nc, dist + 1))
                            visit[nr][nc] = dist + 1  # 방문처리

                            # for tr in range(1, n + 1):
                            #     for tc in range(1, n + 1):
                            #         print(f'{visit[tr][tc]:<3}', end=' ')
                            #     print()
                people[i].r = fr
                people[i].c = fc
                if fr == conv[i][0] and fc == conv[i][1]:
                    next_wall[fr][fc] = 1  # 다음 벽 정보에서 벽으로 변경
                    people[i].done = True  # 완료 변경
                    person_done += 1  # 끝난 사람 추가

    wall = next_wall  # 모든 사람이 이동한 후 벽 갱신

def move_conv_before():
    global wall, person_done, people_visit
    next_wall = copy.deepcopy(wall)
    # 도착하지 않은 사람 마다 이동
    for i in range(1, m + 1):
        if people[i].done == False:
            if people[i].r != 0 and people[i].c != 0:  # 격자에 올려진 경우
                min_dist = INF
                cr = people[i].r
                cc = people[i].c
                fr = 0
                fc = 0
                can_person = []
                for j in range(4):
                    nr = cr + dir[j][0]
                    nc = cc + dir[j][1]

                    # 격자 벗어남 패스
                    if nr < 1 or n < nr or nc < 1 or n < nc:
                        continue
                    if wall[nr][nc] == 1:  # 이미 벽인 경우 패스
                        continue
                    # if people_visit[i][nr][nc] == 1:  # 방문한 위치인 경우 패스
                    #     continue
                    # 편의점과 다음 위치의 거리 측정
                    dist = abs(conv[i][0] - nr) + abs(conv[i][1] - nc)
                    can_person.append((dist, j, nr, nc))
                    # if dist < min_dist:  # 가장 가까우며 우선순위 높은 방향 선정
                    #     min_dist = dist
                    #     fr = nr
                    #     fc = nc
                # print(len(can_person))
                heapq.heapify(can_person)
                while can_person:
                    _, _, tmp_r, tmp_c = heapq.heappop(can_person)
                    if people_visit[i][tmp_r][tmp_c] == 0:  # 방문하지 않은 곳 선택
                        fr = tmp_r
                        fc = tmp_c
                        break
                # _, _, fr, fc = can_person[0]
                # print(i, fr, fc)
                assert fr != 0 and fc != 0
                # 사람 이동
                people[i].r = fr
                people[i].c = fc
                people_visit[i][fr][fc] = 1  # 방문 처리
                # 편의점에 도착한 경우
                if fr == conv[i][0] and fc == conv[i][1]:
                    next_wall[fr][fc] = 1  # 다음 벽 정보에서 벽으로 변경
                    people[i].done = True  # 완료 변경
                    person_done += 1  # 끝난 사람 추가
                # 편의점에 도착하지 않은 경우

    wall = next_wall  # 모든 사람이 이동한 후 벽 갱신

def move_base(time):
    global wall
    sr, sc = conv[time]  # 해당 사람 현위치
    visit = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    q = deque()
    q.append((sr, sc, 0))  # 시작 r, c, 거리 큐
    visit[sr][sc] = 1  # 방문 처리
    min_dist = INF
    can_base = []
    while q:
        cr, cc, dist = q.popleft()
        if dist > min_dist:  # 가까운 베이스 다 찾은 경우
            break
        for i in range(4):
            nr = cr + dir[i][0]
            nc = cc + dir[i][1]
            # 격자 벗어남 패스
            if nr < 1 or n < nr or nc < 1 or n < nc:
                continue
            # 방문 위치 패스
            if visit[nr][nc] == 1:
                continue
            # 벽인 경우 패스
            if wall[nr][nc] == 1:
                continue
            # 베이스인 경우 후보로 추가
            if board[nr][nc] == 1:
                min_dist = dist
                can_base.append((nr, nc, dist + 1))
            # 다음 큐에 추가
            q.append((nr, nc, dist + 1))
            visit[nr][nc] = 1  # 방문 처리
    # print(time)
    # print(can_base)
    # 우선순위 베이스 위치 선정
    heapq.heapify(can_base)
    fr, fc, dist = can_base[0]
    # 사람 위치 변경
    people[time].r = fr
    people[time].c = fc
    wall[fr][fc] = 1  # 벽화
    # people_visit[time][fr][fc] = 1  # 방문 처리

def print_map():
    tmp_board = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(1, m + 1):
        r, c = people[i].r, people[i].c
        tmp_board[r][c] = i
        conv_r, conv_c = conv[i]
        tmp_board[conv_r][conv_c] = f'*{i}'

    for r in range(1, n + 1):
        for c in range(1, n + 1):
            if wall[r][c] == 1:
                tmp_board[r][c] = -1

    tmp_board[people[27].r][people[27].c] = 27


    for r in range(1, n + 1):
        for c in range(1, n + 1):
            print(f'{tmp_board[r][c]:<3}', end=' ')
        print()
    print('-' * 20)


n, m = map(int, input().split())
board = [[]]
wall = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
conv = [0]
people = [0]
people_visit = [[[0 for _ in range(n + 1)] for _ in range(n + 1)] for _ in range(m + 1)]

for r in range(n):
    board.append([0] + list(map(int, input().split())))

for _ in range(m):
    r, c = map(int, input().split())
    conv.append((r, c))
    people.append(person())

person_done = 0
time = 0
while True:
    time += 1
    # print(time)
    # 편의점으로 1칸 이동
    # 편의점 도착 후 벽화
    move_conv()
    if time <= m:
        # 베이스캠프로 이동 후 벽화
        move_base(time)

    if person_done == m:
        break
    # print_map()

print(time)