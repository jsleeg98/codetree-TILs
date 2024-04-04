import sys
import copy

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline

MAX_N = 100000

parents = [0 for _ in range(MAX_N + 1)]
auth = [0 for _ in range(MAX_N + 1)]
alert = [1 for _ in range(MAX_N + 1)]
cnt_chat = [set() for _ in range(MAX_N + 1)]

def init(query):
    global cnt_chat
    # parents 초기화
    for i in range(1, N + 1):
        parents[i] = query[i]
    # auth 초기화
    for i in range(N + 1, 2 * N + 1):
        auth[i - N] = query[i]

    # cnt_chat 초기화
    for i in range(1, N + 1):
        chat = i
        cur = i
        for cnt in range(auth[i]):
            if alert[cur] == 0:
                break
            cnt_chat[parents[cur]].add(chat)
            cur = parents[cur]

def print_cnt_chat(cnt_chat):
    for i in range(0, N + 1):
        print(cnt_chat[i])

def change_alert(query):
    chat = query[1]
    if alert[chat] == 1:  # 끄는 경우
        parent = parents[chat]  # 기준 부모
        # 부모 위로 원래 알림이 왔던 것들 다 지우기
        cur_cnt_chat = copy.deepcopy(cnt_chat[chat])
        cur_cnt_chat.add(chat)  # 현재 채팅방 추가
        for c in cur_cnt_chat:
            tmp_chat = c
            tmp_cur = c
            for cnt in range(auth[c]):
                if alert[tmp_cur] == 0:
                    break
                if c in cnt_chat[parents[tmp_chat]]:
                    cnt_chat[parents[tmp_chat]].remove(c)
                    tmp_cur = parents[tmp_cur]
    else:  # 켜는 경우
        alert[chat] = 1  # 알림 켜기
        parent = parents[chat]  # 기준 부모
        # 부모 위로 알림 가능한 경우 추가하기
        cur_cnt_chat = copy.deepcopy(cnt_chat[chat])
        cur_cnt_chat.add(chat)  # 기준 채팅방도 추가하기
        for c in cur_cnt_chat:  # 채팅방 별 다시 알림 처리
            tmp_chat = c
            cur = c
            for cnt in range(auth[c]):
                if alert[cur] == 0:
                    break
                cnt_chat[parents[cur]].add(tmp_chat)
                cur = parents[cur]

def change_auth(query):
    chat, power = query[1], query[2]
    # 현재 채팅방 알림 다 지우기
    tmp_chat = chat
    cur = chat
    for cnt in range(auth[chat]):
        if alert[cur] == 0:
            break
        if tmp_chat in cnt_chat[parents[cur]]:
            cnt_chat[parents[cur]].remove(tmp_chat)
        cur = parents[cur]

    # 세기 갱신
    auth[chat] = power

    # 현재 채팅방 알림 다시 갱신
    tmp_chat = chat
    cur = chat
    for cnt in range(auth[chat]):
        if alert[cur] == 0:
            break
        cnt_chat[parents[cur]].add(tmp_chat)
        cur = parents[cur]

def change_parent(query):
    c1, c2 = query[1], query[2]
    # 양쪽 위에 다 지우기
    # 현재 채팅방 알림 다 지우기
    parent = parents[c1]  # 기준 부모
    # 부모 위로 원래 알림이 왔던 것들 다 지우기
    cur_cnt_chat = copy.deepcopy(cnt_chat[c1])
    cur_cnt_chat.add(c1)  # 현재 채팅방 추가
    while True:  # 맨 위까지 탐색
        for c in cur_cnt_chat:
            if c in cnt_chat[parent]:
                cnt_chat[parent].remove(c)  # 해당 채팅방 삭제
        parent = parents[parent]
        if parent == 0:
            break

    parent = parents[c2]  # 기준 부모
    # 부모 위로 원래 알림이 왔던 것들 다 지우기
    cur_cnt_chat = copy.deepcopy(cnt_chat[c2])
    cur_cnt_chat.add(c2)  # 현재 채팅방 추가
    while True:  # 맨 위까지 탐색
        for c in cur_cnt_chat:
            if c in cnt_chat[parent]:
                cnt_chat[parent].remove(c)  # 해당 채팅방 삭제
        parent = parents[parent]
        if parent == 0:
            break


    # 부모 변경
    c1_parent = parents[c1]
    c2_parent = parents[c2]
    parents[c1] = c2_parent
    parents[c2] = c1_parent

    # 양쪽 위에 알림 갱신
    cur_cnt_chat = copy.deepcopy(cnt_chat[c1])
    cur_cnt_chat.add(c1)  # 기준 채팅방도 추가하기
    for c in cur_cnt_chat:  # 채팅방 별 다시 알림 처리
        tmp_chat = c
        cur = c
        for cnt in range(auth[c]):
            if alert[cur] == 0:
                break
            cnt_chat[parents[cur]].add(tmp_chat)
            cur = parents[cur]

    cur_cnt_chat = copy.deepcopy(cnt_chat[c2])
    cur_cnt_chat.add(c2)  # 기준 채팅방도 추가하기
    for c in cur_cnt_chat:  # 채팅방 별 다시 알림 처리
        tmp_chat = c
        cur = c
        for cnt in range(auth[c]):
            if alert[cur] == 0:
                break
            cnt_chat[parents[cur]].add(tmp_chat)
            cur = parents[cur]

def check(query):
    chat = query[1]

    print(len(cnt_chat[chat]))

N, Q = map(int, input().split())

for _ in range(Q):
    query = list(map(int, input().split()))
    # print(query)
    if query[0] == 100:
        init(query)
        # print_cnt_chat(cnt_chat)
    elif query[0] == 200:
        change_alert(query)
        # print_cnt_chat(cnt_chat)
    elif query[0] == 300:
        change_auth(query)
        # print_cnt_chat(cnt_chat)
    elif query[0] == 400:
        change_parent(query)
        # print_cnt_chat(cnt_chat)
    elif query[0] == 500:
        check(query)