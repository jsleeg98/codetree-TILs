import sys
from collections import defaultdict

class Box:
    def __init__(self):
        self.front = -1
        self.back = -1
        self.weight = 0

def make_factory(query):
    global belt_front_back, box_status, belt_status, num_belt, num_box
    n = query[1]
    m = query[2]
    num_belt = m
    num_box = n
    cnt_belt = n // m  # 한 벨트랑 적재되는 물건 수
    tmp_id = [[] for _ in range(11)]
    tmp_w = [[] for _ in range(11)]
    for i, q in enumerate(query[3:3 + n]):  # id 분리
        tmp_id[(i // cnt_belt) + 1].append(q)
        box_status[q] = 1  # 박스 상태 온
    for i, q in enumerate(query[3 + n:]):
        tmp_w[(i // cnt_belt) + 1].append(q)
    # print(tmp_id)
    # print(tmp_w)
    # print()

    for i in range(1, m + 1):
        belt_status[i] = 1  # 벨트 상태 온
        front = -i
        for k in range(0, cnt_belt - 1):
            box_list[tmp_id[i][k]] = Box()
            box_list[tmp_id[i][k]].front = front
            box_list[tmp_id[i][k]].back = tmp_id[i][k + 1]
            box_list[tmp_id[i][k]].weight = tmp_w[i][k]
            front = tmp_id[i][k]
        box_list[tmp_id[i][-1]] = Box()
        box_list[tmp_id[i][-1]].front = front
        box_list[tmp_id[i][-1]].back = -i
        box_list[tmp_id[i][-1]].weight = tmp_w[i][-1]
        belt_front_back.append([tmp_id[i][0], tmp_id[i][-1]])

    # print(belt_front_back)
    # print()

def unload_box(query):
    global belt_front_back, box_list, box_status
    w_max = query[1]
    total_weight = 0
    for i in range(1, num_belt + 1):
        if belt_status[i] == 0:  # 해당 벨트 망가진 경우 패스
            continue
        front_id = belt_front_back[i][0]
        if front_id == 937032277:
            print()
        if front_id < 0:  # 벨트가 비어있는 경우
            continue
        # 상자 내리기
        if box_list[front_id].weight <= w_max:
            belt_front_back[i][0] = box_list[front_id].back  # 해당 벨트 맨 앞 상자 id 변경
            box_status[front_id] = 0  # 박스 상태 끄기
            total_weight += box_list[front_id].weight
        # 맨 뒤로 보내기
        else:
            belt_front_back[i][0] = box_list[front_id].back  # 해당 벨트 맨 앞 상자 id 변경
            box_list[box_list[front_id].back].front = -i  # 두번째 상자 front -belt idx 로 변경
            box_list[belt_front_back[i][1]].back = front_id  # 맨 뒤 상자 back을 front_id로 변경
            box_list[front_id].front = belt_front_back[i][1]  # 맨 앞 상자 front 변경
            belt_front_back[i][1] = front_id  # 해당 벨트 맨 뒤 상자 id 변경

    print(total_weight)
    # print(belt_front_back)
    # print()

def remove_box(query):
    global belt_front_back, box_list, box_status
    r_id = query[1]
    if box_status[r_id] == 0:
        print(-1)
    else:
        print(r_id)
        box_status[r_id] = 0  # 박스 상태 끄기
        if box_list[r_id].front < 0:  # 맨 앞 상자인 경우
            belt_idx = -box_list[r_id].front
            belt_front_back[belt_idx][0] = box_list[r_id].back
            box_list[box_list[r_id].back].front = -belt_idx
        elif box_list[r_id].back < 0:  # 맨 뒤 상자인 경우
            belt_idx = -box_list[r_id].back
            belt_front_back[belt_idx][1] = box_list[r_id].front
            box_list[box_list[r_id].front].back = -belt_idx
        else:  # 중간 상자였던 경우
            front_box_id = box_list[r_id].front
            back_box_id = box_list[r_id].back
            box_list[front_box_id].back = back_box_id
            box_list[back_box_id].front = front_box_id

def check_box(query):
    global belt_front_back, box_list, box_status
    f_id = query[1]
    if box_status[f_id] == 0:
        print(-1)
    else:
        cur_id = f_id
        # 현재 상자가 있는 벨트 찾기
        while cur_id > 0:
            cur_id = box_list[cur_id].front
        belt_idx = -cur_id
        # print(belt_idx)
        # print(belt_front_back)
        # 해당 벨트에서 맨 앞으로 가져오기
        if belt_front_back[belt_idx][0] != f_id:  # 원래 맨 앞이 아니었던 경우
            if box_list[f_id].back < 0:  # 맨 뒤였던 경우
                front_id = box_list[f_id].front
                box_list[front_id].back = -belt_idx
                belt_front_back[belt_idx][1] = front_id  # 벨트 맨 뒤 정보 갱신
            else:  # 중간이었던 경우
                # 기존 위치 앞뒤 붙이기
                print(f_id)
                # if f_id == 937032277:
                #     print()
                front_box_id = box_list[f_id].front
                back_box_id = box_list[f_id].back
                # print(front_box_id)
                box_list[front_box_id].back = back_box_id
                box_list[back_box_id].front = front_box_id
            # 맨 앞 바꾸기
            before_front_id = belt_front_back[belt_idx][0]  # 기존의 맨앞 상자 id
            box_list[before_front_id].front = f_id  # 기존 맨 앞 상자 front에 f_id 갱신
            box_list[f_id].front = -belt_idx  # f_id에 벨트 정보 갱신
            box_list[f_id].back = before_front_id  # f_id back에 기존 맨 앞 상자 id 갱신
            belt_front_back[belt_idx][0] = f_id  # 벨트 맨 앞 정보 갱신

def break_belt(query):
    global belt_front_back, belt_status, box_list
    b_num = query[1]
    if belt_status[b_num] == 0:  # 이미 부서진 상태인 경우
        print(-1)
    else:  # 부서지지 않은 경우
        print(b_num)
        # 다음 벨트 찾기
        nxt_b_num = ((b_num) % num_belt) + 1
        while True:
            if belt_status[nxt_b_num] == 1:
                break
            nxt_b_num = ((nxt_b_num + 1) % num_belt) + 1

        belt_status[b_num] = 0  # 현재 벨트 고장 상태 변환

        if belt_front_back[b_num][0] > 0:  # 고장난 벨트에 물건이 있는 경우
            # 고장난 벨트 맨 앞을 새로운 벨트 맨뒤로 붙이기
            if belt_front_back[b_num][0] > 0:  # 옮길 벨트에 물건이 있는 경우
                broken_front_id = belt_front_back[b_num][0]  # 고장난 벨트의 맨 앞 id
                broken_back_id = belt_front_back[b_num][1]  # 고장난 벨트의 맨 뒤 id
                new_back_id = belt_front_back[nxt_b_num][1]  # 새로운 벨트의 맨 뒤 id
                box_list[new_back_id].back = broken_front_id  # 새로운 벨트 맨 뒤에 붙이기
                box_list[broken_front_id].front = new_back_id  # 고장난 벨트 맨 앞 상자 붙이기
                box_list[broken_back_id].back = -nxt_b_num  # 맨뒤의 벨트 정보 바꾸기
                belt_front_back[nxt_b_num][1] = broken_back_id  # 새로운 벨트 맨 뒤 정보 갱신
            else:  # 옮길 벨트에 물건이 없는 경우
                broken_front_id = belt_front_back[b_num][0]  # 고장난 벨트의 맨 앞 id
                broken_back_id = belt_front_back[b_num][1]  # 고장난 벨트의 맨 뒤 id
                belt_front_back[nxt_b_num][0] = broken_front_id
                belt_front_back[nxt_b_num][1] = broken_back_id





num_belt = 0
num_box = 0
belt_front_back = [[]]  # 각 벨트 위 맨앞 맨뒤 상태 idx 저장
# box_list = [Box() for _ in range(1000000001)]  # 박스 객체 리스트, idx는 id
# box_status = [0 for _ in range(1000000001)]  # 박스 상태 리스트, idx는 id
box_list = defaultdict(int)
box_status = defaultdict(int)
belt_status = [0 for _ in range(11)]  # 벨트 상태 리스트, idx는 벨트 번호
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