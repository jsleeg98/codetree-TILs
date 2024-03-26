import sys
import heapq

input = sys.stdin.readline

class Person:
    def __init__(self, r, c):
        self.r = r
        self.c = c


li_p = []
m = []
ext = None
N, M, K = map(int, input().split())
m.append(['x'] * (N + 1))
for _ in range(N):
    m.append(['x'] + list(map(int, input().split())))
for _ in range(M):
    r, c = map(int, input().split())
    tmp = Person(r, c)
    li_p.append(tmp)
ext = list(map(int, input().split()))

# for r in range(N + 1):
#     for c  in range(N + 1):
#         print(m[r][c], end=' ')
#     print()

# for i in range(M):
#     print(li_p[i].r, li_p[i].c)
#
# print(ext)

def move(li_p, ext, total_move):
    li_p_new = []
    for p in li_p:
        cr = p.r
        cc = p.c
        dist = abs(cr - ext[0]) + abs(cc - ext[1])
        flag = True
        for i in range(4):
            nr = cr + dir[i][0]
            nc = cc + dir[i][1]
            if nr < 1 or nc < 1 or nr > N or nc > N:  # 미로 밖
                continue
            if m[nr][nc] != 0:  # 벽
                continue
            if nr == ext[0] and nc == ext[1]:  # 출구 나간 경우
                total_move += 1
                flag = False
                break
            # 못 나가고 움직인 경우
            if (abs(nr - ext[0]) + abs(nc - ext[1])) < dist:
                flag = False
                p.r = nr
                p.c = nc
                li_p_new.append(p)
                total_move += 1
                break
        if flag:  # 못 나가고 못 음직인 겨우
            li_p_new.append(p)
    return li_p_new, total_move

def print_p(li_p):
    for p in li_p:
        print(p.r, p.c)

def print_m(m):
    for r in range(1, N + 1):
        for c  in range(1, N + 1):
            print(m[r][c], end=' ')
        print()

def rotate(li_p, ext, m):
    # 가까운 사람 선별
    dist = 1e9
    li_p_min = []
    for p in li_p:
        tmp_dist = max(abs(p.r - ext[0]), abs(p.c - ext[1]))
        if dist > tmp_dist:
            li_p_min = [p]
            dist = tmp_dist
        elif dist == tmp_dist:
            li_p_min.append(p)

    li_rect = []
    cr = ext[0] - dist
    cc = ext[1] - dist
    for dr in range(0, dist + 1):
        for dc in range(0, dist + 1):
            rect_r = cr + dr
            rect_c = cc + dc
            # print(rect_r, rect_c)
            if 1 <= rect_r <= N and 1 <= rect_c <= N and 1 <= rect_r + dist <= N and 1 <= rect_c + dist <= N:
                for p in li_p_min:
                    if rect_r <= p.r <= rect_r + dist and rect_c <= p.c <= rect_c + dist:
                        li_rect.append((rect_r, rect_c))
                        break

    # for d in range(dist, -1, -1):
    #     rect_r = ext[0] - dist
    #     rect_c = ext[1] - d
    #     if 1 <= rect_r <= N and 1 <= rect_c <= N and 1 <= rect_r + dist <= N and 1 <= rect_c + dist <= N:
    #         for p in li_p_min:
    #             if rect_r <= p.r <= rect_r + dist and rect_c <= p.c <= rect_c + dist:
    #                 li_rect.append((rect_r, rect_c))
    #                 break
    # for d in range(dist-1, -1, -1):
    #     rect_r = ext[0] - d
    #     rect_c = ext[1]
    #     if 1 <= rect_r <= N and 1 <= rect_c <= N and 1 <= rect_r + dist <= N and 1 <= rect_c + dist <= N:
    #         for p in li_p_min:
    #             if rect_r <= p.r <= rect_r + dist and rect_c <= p.c <= rect_c + dist:
    #                 li_rect.append((rect_r, rect_c))
    #                 break
    # for d in range(1, dist + 1):
    #     rect_r = ext[0]
    #     rect_c = ext[1] - d
    #     if 1 <= rect_r <= N and 1 <= rect_c <= N and 1 <= rect_r + dist <= N and 1 <= rect_c + dist <= N:
    #         for p in li_p_min:
    #             if rect_r <= p.r <= rect_r + dist and rect_c <= p.c <= rect_c + dist:
    #                 li_rect.append((rect_r, rect_c))
    #                 break
    # for d in range(1, dist):
    #     rect_r = ext[0] - d
    #     rect_c = ext[1] - dist
    #     if 1 <= rect_r <= N and 1 <= rect_c <= N and 1 <= rect_r + dist <= N and 1 <= rect_c + dist <= N:
    #         for p in li_p_min:
    #             if rect_r <= p.r <= rect_r + dist and rect_c <= p.c <= rect_c + dist:
    #                 li_rect.append((rect_r, rect_c))
    #                 break

    # 돌릴 정사각형 왼쪽 위 좌표 찾기
    heapq.heapify(li_rect)  # r, c 우선순위로 정렬

    # 현재 사람 위치 맵 그리기
    m_p = [[[] for _ in range(N + 1)] for _ in range(N + 1)]
    for p in li_p:
        m_p[p.r][p.c].append(p)
    # print(li_rect)
    tr = li_rect[0][0]
    tc = li_rect[0][1]

    # print(f'사각형 {tr}, {tc}, {dist}')
    # 새로운 맵 저장
    new_m = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
    for dr in range(0, dist + 1):
        for dc in range(0, dist + 1):
            cr = tr + dr
            cc = tc + dc
            nr = cr + (dc - dr)
            nc = cc + (dist - dr - dc)
            # print('-' * 20)
            # print(cr, cc)
            # print(nr, nc)
            # print('-' * 20)
            if len(m_p[cr][cc]) > 0:  # 사람 위치 인 경우
                for p in m_p[cr][cc]:
                    p.r = nr
                    p.c = nc
                    # print('person')
            elif cr == ext[0] and cc == ext[1]:  # 출구 위치인 경우
                next_ext_r = nr
                next_ext_c = nc
            elif m[cr][cc] != 0:  # 벽이 있는 경우
                new_m[nr][nc] = m[cr][cc] - 1
            else:
                new_m[nr][nc] = m[cr][cc]
    ext[0] = next_ext_r
    ext[1] = next_ext_c
    for dr in range(0, dist + 1):
        for dc in range(0, dist + 1):
            cr = tr + dr
            cc = tc + dc
            m[cr][cc] = new_m[cr][cc]

    return m, li_p

dir = ((1, 0), (-1, 0), (0, 1), (0, -1))
total_move = 0
for i in range(K):
    # print(f'{i + 1}초')
    # print_m(m)
    # print_p(li_p)
    # print('-' * 20)
    if len(li_p) == 0:  # 모두 탈출한 경우 끝
        break
    li_p, total_move = move(li_p, ext, total_move)  # 움직임
    # print('move')
    # print_p(li_p)
    if len(li_p) == 0:
        break
    m, li_p = rotate(li_p, ext, m)
    # print(f'{i + 1}초 후')
    # print(total_move)
    # print_p(li_p)
    # print_m(m)
    # print('-' * 20)

print(total_move)
print(ext[0], ext[1])