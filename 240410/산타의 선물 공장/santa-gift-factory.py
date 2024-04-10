import sys
from collections import defaultdict

# sys.stdin = open('input.txt', 'r')

class Box:
    def __init__(self):
        self.front = 0
        self.back = 0
        self.weight = 0
        self.belt = 0

    # def __str__(self):
    #     print(f'belt: {self.belt} | front: {self.front} | back: {self.back} | weight: {self.weight}')

MAX_M = 10
head = [0 for _ in range(MAX_M + 1)]
tail = [0 for _ in range(MAX_M + 1)]
box_list = defaultdict(lambda : 0)
belt_state = [False] * (MAX_M + 1)
box_state = defaultdict(lambda: 0)

def make_factory(query):
    global n, m, belt_state, box_state, box_list, head, tail
    n = query[1]
    m = query[2]
    ids, ws = query[3:3+n], query[3+n:3+n+n]

    size = n // m
    for i in range(1, m + 1):
        tmp_id = ids[size * (i - 1)]
        box_list[tmp_id] = Box()
        head[i] = tmp_id
        belt_state[i] = True
        for j in range(size - 1):
            tmp_id = ids[size * (i - 1) + j]
            box_list[ids[size * (i - 1) + j + 1]] = Box()
            box_list[tmp_id].back = ids[size * (i - 1) + j + 1]
            box_list[tmp_id].weight = ws[size * (i - 1) + j]
            box_list[ids[size * (i - 1) + j + 1]].front = tmp_id
            box_list[tmp_id].belt = i
            box_state[tmp_id] = True
        box_list[ids[size * i - 1]].belt = i
        box_list[ids[size * i - 1]].weight = ws[size * i - 1]
        tail[i] = ids[size * i - 1]
        box_state[ids[size * i - 1]] = True

    # for key in box_list.keys():
    #     print(f'{key} | belt: {box_list[key].belt} | front: {box_list[key].front} | back: {box_list[key].back} | weight: {box_list[key].weight}')
    # print()

    # for i in range(1, m + 1):
    #     print(f'{i} | head : {head[i]}')
    #     print(f'{i} | tail : {tail[i]}')
    # print()

# 삭제 함수
def remove(id):
    global box_state, head, box_list, tail
    belt_idx = box_list[id].belt

    # 하나 밖에 안남은 경우
    if head[belt_idx] == tail[belt_idx]:
        head[belt_idx] = 0
        tail[belt_idx] = 0
    # 맨 앞을 삭제하는 경우
    elif head[belt_idx] == id:
        # head 갱신
        head[belt_idx] = box_list[id].back
        # 두 번째 box front 수정
        box_list[box_list[id].back].front = 0
    # 맨 뒤를 삭제하는 경우
    elif tail[belt_idx] == id:
        # tail 갱신
        tail[belt_idx] = box_list[id].front
        # 뒤어서 두번째 box back 수정
        box_list[box_list[id].front].back = 0
    # 중간을 삭제하는 경우
    else:
        # 앞 box의 back 갱신
        box_list[box_list[id].front].back = box_list[id].back
        # 뒤 box의 front 갱신
        box_list[box_list[id].back].front = box_list[id].front

    box_state[id] = False
    box_list[id].front = 0
    box_list[id].back = 0

def push_box(front_id, input_id):
    global box_list, tail
    box_list[front_id].back = input_id
    box_list[input_id].front = front_id

    belt_idx = box_list[front_id].belt
    # 맨 뒤에 넣는 경우
    if tail[belt_idx] == front_id:
        # tail 갱신
        tail[belt_idx] = input_id

def unload_box(query):
    global belt_state, box_list, head, tail
    w_max = query[1]

    ans = 0
    for i in range(1, m + 1):
        if belt_state[i] == False:  # 벨트가 망가진 경우 패스
            continue
        # 해당 벨트 내에 물건이 하나 이상 있는 경우
        if head[i] != 0:
            _id = head[i]
            # 내리는 경우
            if box_list[_id].weight <= w_max:
                ans += box_list[_id].weight
                remove(_id)
                box_list[_id].belt = 0  # 벨트에서 내림


            # 맨 뒤로 넘기는 경우
            elif box_list[_id].back != 0:  # 하나밖에 남은 경우가 아닌 경우
                remove(_id)
                push_box(tail[i], _id)
                box_state[_id] = True
            # 하나면 그대로
            # for key in box_list.keys():
            #     print(
            #         f'{key} | belt: {box_list[key].belt} | front: {box_list[key].front} | back: {box_list[key].back} | weight: {box_list[key].weight}')
            # print()
    print(ans)

def remove_box(query):
    global box_state
    r_id = query[1]

    if box_state[r_id] == True:
        remove(r_id)
        print(r_id)
    else:
        print(-1)

def check_box(query):
    global box_state, box_list, head, tail
    f_id = query[1]

    if box_state[f_id] == True:
        belt_idx = box_list[f_id].belt
        print(belt_idx)
        if head[belt_idx] != f_id:  # 원래 맨 앞이 아닌 경우
            ori_head = head[belt_idx]
            ori_tail = tail[belt_idx]
            # 벨트 head f_id로 갱신
            head[belt_idx] = f_id
            # 벨트 tail f_id.front로 갱신
            tail[belt_idx] = box_list[f_id].front
            # f_id.front의 back 0 갱신
            box_list[box_list[f_id].front].back = 0
            # f_id.front = 0 갱신
            box_list[f_id].front = 0
            # 기존 tail의 back 기존 head로 갱신
            box_list[ori_tail].back = ori_head
            # 기존 head의 front 기존 tail로 갱신
            box_list[ori_head].front = ori_tail
    else:
        print(-1)

def break_belt(query):
    global belt_state, head, tail, box_state, box_list
    b_num = query[1]

    if belt_state[b_num] == False:
        print(-1)
    else:
        print(b_num)
        belt_state[b_num] = False
        # 현 벨트에 물건이 있는 경우
        if head[b_num] != 0 and tail[b_num] != 0:
            nxt_b_num = (b_num % m) + 1
            while True:
                if belt_state[nxt_b_num] == True:
                    break
                nxt_b_num = (nxt_b_num % m) + 1
            # 옮길 벨트에 아무것도 없는 경우
            if head[nxt_b_num] == 0 and tail[nxt_b_num] == 0:
                # 옮길 벨트의 head 갱신
                head[nxt_b_num] = head[b_num]
                # 옮길 벨트의 tail 갱신
                tail[nxt_b_num] = tail[b_num]
            # 옮길 벨트에 물건이 있는 경우
            else:
                # # 옮길 벨트의 tail box의 back에 현 벨트의 head 갱신
                # box_list[tail[nxt_b_num]].back = head[b_num]
                # # 현 벨트의 head의 front에 옮길 벨트의 tail 갱신
                # box_list[head[b_num]].front = tail[nxt_b_num]
                push_box(tail[nxt_b_num], head[b_num])
                # 옮길 벨트의 tail 현 벨트의 tail로 갱신
                tail[nxt_b_num] = tail[b_num]

            head[b_num] = 0
            tail[b_num] = 0

            # 벨트 정보 갱신
            cur_id = head[nxt_b_num]
            while cur_id != 0:
                box_list[cur_id].belt = nxt_b_num
                cur_id = box_list[cur_id].back






n = 0
m = 0
Q = int(input())
for _ in range(Q):
    query = list(map(int, input().split()))
    # print(query)
    if query[0] == 100:
        make_factory(query)
    elif query[0] == 200:
        unload_box(query)
    elif query[0] == 300:
        remove_box(query)
    elif query[0] == 400:
        check_box(query)
    elif query[0] == 500:
        break_belt(query)
    # for key in box_list.keys():
    #     print(f'{key} | belt: {box_list[key].belt} | front: {box_list[key].front} | back: {box_list[key].back} | weight: {box_list[key].weight}')
    # print()