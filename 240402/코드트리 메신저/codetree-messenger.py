import sys
from collections import deque

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline


def init(query):
    global P, A, C
    (empty, tmp_p, tmp_a) = query[0], query[1 : N + 1], query[N + 1:]
    P += tmp_p
    A += tmp_a
    # 자식 정보 갱신
    for i, p in enumerate(P[1:]):
        C[p].append(i + 1)

def change_noti(query):
    chat = query[1]
    noti[chat] = (noti[chat] + 1) % 2

def change_auth(query):
    chat, power = query[1], query[2]
    A[chat] = power

def change_p(query):
    global P, C
    chat1, chat2 = query[1], query[2]

    # 부모 변경
    chat1_p = P[chat1]
    chat2_p = P[chat2]
    P[chat1] = chat2_p
    P[chat2] = chat1_p
    # 자식 변경
    C[chat2_p].remove(chat2)
    C[chat1_p].remove(chat1)
    C[chat2_p].append(chat1)
    C[chat1_p].append(chat2)


def check(query):
    chat = query[1]
    q = deque()
    for tmp_cc in C[chat]:
        if noti[tmp_cc] == 1:
            q.append((tmp_cc, 1))
    cnt = 0
    while q:
        tmp_c, depth = q.popleft()
        if noti[tmp_c] == 0:  # 알림이 꺼져있는 경우
            continue
        if depth <= A[tmp_c]:  # 도달 불가능한 경우
            cnt += 1
        for tmp_cc in C[tmp_c]:
            q.append((tmp_cc, depth + 1))

    print(cnt)

N, Q = map(int, input().split())

P = [0]  # 부모 저장
A = [0]  # auth 저장
C = [[] for _ in range(N + 1)]  # 자식 저장
noti = [1 for _ in range(N + 1)]

for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 100:
        init(query)
        # print(P)
        # print(C)
        # print(A)
    elif query[0] == 200:
        change_noti(query)
    elif query[0] == 300:
        change_auth(query)
    elif query[0] == 400:
        change_p(query)
    elif query[0] == 500:
        check(query)