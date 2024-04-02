import sys
from collections import deque

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline

class knight:
    def __init__(self, r, c, h, w, k):
        self.r = r
        self.c = c
        self.h = h
        self.w = w
        self.k = k
        self.damage = 0
        self.s = True

dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def move_check(id, d):
    # knight 맵 만들기
    m_k = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
    m_k_tmp = [[0 for _ in range(L + 1)] for _ in range(L + 1)]

    for i in range(1, N + 1):
        tmp = li_k[i]
        if tmp.s == False:  # 죽은 경우 패스
            continue
        s_r, s_c = tmp.r, tmp.c
        for r in range(s_r, s_r + tmp.h):
            for c in range(s_c, s_c + tmp.w):
                m_k[r][c] = i

    # knight 이동 가능 여부 체크
    # 벽 체크
    # 기사 체크
    flag = True
    moved_k = []  # 움직인 기사 id 저장
    damage_k = [0 for _ in range(N + 1)]
    moved_k.append(id)
    move_k = deque()
    move_k.append(id)
    while move_k:
        id = move_k.popleft()
        cur_k = li_k[id]
        if cur_k.s == False:
            continue
        for r in range(cur_k.r, cur_k.r + cur_k.h):
            for c in range(cur_k.c, cur_k.c + cur_k.w):
                nr = r + dir[d][0]
                nc = c + dir[d][1]
                if nr < 1 or L < nr or nc < 1 or L < nc:  # 맵을 벗어난 경우
                    flag = False  # 움직이지 못함 표시
                    break
                if m[nr][nc] == 2:  # 맵의 벽인 경우
                    flag = False  # 움직이지 못함 표시
                    break
                if m[nr][nc] == 1:
                    damage_k[id] += 1
                if m_k[nr][nc] != id and m_k[nr][nc] != 0:  # 해당 칸에 다른 기사가 있는 경우
                    if not m_k[nr][nc] in move_k:  # 움직일 기사에 처음 들어오는 경우
                        move_k.append(m_k[nr][nc])  # 움직일 기사에 추가
                        moved_k.append(m_k[nr][nc])
                m_k_tmp[nr][nc] = id
            if flag == False:  # 움직이지 못할 경우 종료
                break

    return flag, m_k_tmp, moved_k, damage_k

def move_damage(id, d, moved_k, damage_k):
    # id 기사는 데미지 안입음
    # moved_k 기사는 움직임
    for tmp_id in moved_k:
        li_k[tmp_id].r += dir[d][0]
        li_k[tmp_id].c += dir[d][1]
        if tmp_id == id:  # 명령받은 기사는 패스
            continue
        li_k[tmp_id].damage += damage_k[tmp_id]  # 피해 데미지 누적
        li_k[tmp_id].k -= damage_k[tmp_id]  # 체력 감소
        if li_k[tmp_id].k <= 0:  # 체력이 0 이하이면 죽음
            li_k[tmp_id].s = False


def print_map(m):
    for r in range(1, L + 1):
        for c in range(1, L + 1):
            print(m[r][c], end=' ')
        print()

def print_k(li_k):
    tmp_m = [[0 for _ in range(L + 1)] for _ in range(L + 1)]
    for i, k in enumerate(li_k[1:]):
        if k.s:
            for r in range(k.r, k.r + k.h):
                for c in range(k.c, k.c + k.w):
                    tmp_m[r][c] = i + 1
    print_map(tmp_m)

L, N, Q = map(int, input().split())

m = [[]]
li_k = [0]

for _ in range(L):
    m.append([2] + list(map(int, input().split())))

for _ in range(N):
    r, c, h, w, k = map(int, input().split())
    li_k.append(knight(r, c, h, w, k))

for _ in range(Q):
    id, d = map(int, input().split())
    flag, m_k_tmp, moved_k, damage_k = move_check(id, d)
    # print(f'flag : {flag}')
    if flag:
        move_damage(id, d, moved_k, damage_k)
    # print_k(li_k)

ans = 0
for k in li_k[1:]:
    if k.s:
        ans += k.damage
print(ans)