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
    # 도착하지 않은 사람 마다 이동
    for i in range(1, m + 1):
        if people[i].done == False:
            min_dist = INF
            cr = people[i].r
            cc = people[i].c
            fr = 0
            fc = 0
            for j in range(4):
                nr = cr + dir[j][0]
                nc = cc + dir[j][1]
                # 격자 벗어남 패스
                if nr < 1 or n < nr or nc < 1 or n < nc:
                    continue
                if wall[nr][nc] == 1:  # 이미 벽인 경우 패스
                    continue
                # 편의점과 다음 위치의 거리 측정
                dist = abs(conv[i][0] - nr) + abs(conv[i][1] - nc)
                if dist < min_dist:  # 가장 가까우며 우선순위 높은 방향 선정
                    min_dist = dist
                    fr = nr
                    fc = nc
            # 사람 이동
            people[i].r = fr
            people[i].c = fc
            # 편의점에 도착한 경우
            if fr == conv[i][0] and fc == conv[i][1]:
                next_wall[fr][fc] = 1  # 벽으로 변경
                people[i].done = True
                person_done += 1
            # 편의점에 도착하지 않은 경우

    wall = next_wall  # 모든 사람이 이동한 후 벽 갱신

def move_base(time):
    global wall
    sr, sc = conv[time]
    visit = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    q = deque()
    q.append((sr, sc, 0))  # 시작 r, c, 거리 큐
    visit[sr][sc] = 1  # 방문처리
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
            visit[nr][nc] = 1

    # 우선순위 베이스 위치 선정
    heapq.heapify(can_base)
    fr, fc, dist = can_base[0]
    # 사람 위치 변경
    people[time].r = fr
    people[time].c = fc
    wall[fr][fc] = 1  # 벽화

def print_map(m):
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            print(m[r][c], end=' ')
        print()
    print('-' * 20)

n, m = map(int, input().split())
board = [[]]
wall = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
conv = [0]
people = [0]

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
    # 편의점으로 1칸 이동
    # 편의점 도착 후 벽화
    move_conv()
    if time <= m:
        # 베이스캠프로 이동 후 벽화
        move_base(time)

    if person_done == m:
        break

print(time)