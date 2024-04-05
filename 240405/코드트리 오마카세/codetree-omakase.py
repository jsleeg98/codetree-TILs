import sys

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline


def t2idx(idx, t):
    return (idx - ((t-1) % L)) % L

def add_sushi(query):
    global sushi_name, sushi_cnt, ans_s, ans_p, people
    t, x, name = int(query[1]), int(query[2]), query[3]

    idx = t2idx(x, t)
    if name in sushi_name[idx]:
        name_idx = 0
        for i in range(len(sushi_name[idx])):
            if name == sushi_name[idx][i]:
                name_idx = i
                break
        sushi_cnt[idx][name_idx] += 1
    else:
        sushi_name[idx].append(name)
        sushi_cnt[idx].append(1)
    ans_s += 1

    for key, value in people.items():
        # 현 위치 idx
        idx = t2idx(value[0], t)
        # 사람 위치의 초밥 정보
        tmp_sushi_names = sushi_name[idx]
        tmp_sushi_cnts = sushi_cnt[idx]
        # 먹어야할 초밥 수
        tmp_cnt = value[1]
        if key in tmp_sushi_names:  # 같은 위치에 사람과 초밥이 있는 경우
            name_idx = 0
            for i in range(len(sushi_name[idx])):
                if key == sushi_name[idx][i]:
                    name_idx = i
                    break
            tmp_sushi_cnt = tmp_sushi_cnts[name_idx]  # 있는 초밥 수
            # 초밥의 수가 더 많은 경우
            if tmp_cnt < tmp_sushi_cnt:
                sushi_cnt[idx][name_idx] -= tmp_cnt  # 초밥 상태만 변경
                ans_p -= 1  # 전체 사람 수 감소
                ans_s -= tmp_cnt  # 전체 초밥 수 감소
                # del people[key]  # 현재 사람 삭제
            # 먹어야할 수가 더 많은 경우
            elif tmp_cnt > tmp_sushi_cnt:
                value[1] -= tmp_sushi_cnt  # 사람 상태만 변경
                ans_s -= tmp_sushi_cnt  # 전체 초밥 수 감소
                del sushi_name[idx][name_idx]  # 현재 초밥 삭제
                del sushi_cnt[idx][name_idx]  # 현재 초밥 삭제
            # 같은 경우
            else:
                sushi_cnt[idx][name_idx] -= tmp_cnt  # 초밥 상태 변경
                value[1] -= tmp_cnt  # 사람 상태 변경
                ans_p -= 1  # 전체 사람 수 감소
                ans_s -= tmp_cnt  # 전체 초밥 수 감소
                # del people[key]  # 현재 사람 삭제
                del sushi_name[idx][name_idx]  # 현재 초밥 삭제
                del sushi_cnt[idx][name_idx]  # 현재 초밥 삭제

    keys = list(people.keys())
    for key in keys:
        if people[key][1] == 0:
            del people[key]

def print_sushi():
    for i in range(L):
        print(f'{i} : {sushi_cnt[i]}')

def add_person(query):
    global sushi_cnt, sushi_name, people, ans_p, ans_s
    t, x, name, n = int(query[1]), int(query[2]), query[3], int(query[4])
    people[name] = [x, n]
    ans_p += 1

    for key, value in people.items():
        # 현 위치 idx
        idx = t2idx(value[0], t)
        # 사람 위치의 초밥 정보
        tmp_sushi_names = sushi_name[idx]
        tmp_sushi_cnts = sushi_cnt[idx]
        # 먹어야할 초밥 수
        tmp_cnt = value[1]
        if key in tmp_sushi_names:  # 같은 위치에 사람과 초밥이 있는 경우
            name_idx = 0
            for i in range(len(sushi_name[idx])):
                if key == sushi_name[idx][i]:
                    name_idx = i
                    break
            tmp_sushi_cnt = tmp_sushi_cnts[name_idx]  # 있는 초밥 수
            # 초밥의 수가 더 많은 경우
            if tmp_cnt < tmp_sushi_cnt:
                sushi_cnt[idx][name_idx] -= tmp_cnt  # 초밥 상태만 변경
                ans_p -= 1  # 전체 사람 수 감소
                ans_s -= tmp_cnt  # 전체 초밥 수 감소
                # del people[key]  # 현재 사람 삭제
            # 먹어야할 수가 더 많은 경우
            elif tmp_cnt > tmp_sushi_cnt:
                value[1] -= tmp_sushi_cnt  # 사람 상태만 변경
                ans_s -= tmp_sushi_cnt  # 전체 초밥 수 감소
                del sushi_name[idx][name_idx]  # 현재 초밥 삭제
                del sushi_cnt[idx][name_idx]  # 현재 초밥 삭제
            # 같은 경우
            else:
                sushi_cnt[idx][name_idx] -= tmp_cnt  # 초밥 상태 변경
                value[1] -= tmp_cnt  # 사람 상태 변경
                ans_p -= 1  # 전체 사람 수 감소
                ans_s -= tmp_cnt  # 전체 초밥 수 감소
                # del people[key]  # 현재 사람 삭제
                del sushi_name[idx][name_idx]  # 현재 초밥 삭제
                del sushi_cnt[idx][name_idx]  # 현재 초밥 삭제

    keys = list(people.keys())
    for key in keys:
        if people[key][1] == 0:
            del people[key]

def photo(query):
    global sushi_name, sushi_cnt, people, ans_p, ans_s
    t = int(query[1])

    for key, value in people.items():
        # 현 위치 idx
        idx = t2idx(value[0], t)
        # 사람 위치의 초밥 정보
        tmp_sushi_names = sushi_name[idx]
        tmp_sushi_cnts = sushi_cnt[idx]
        # 먹어야할 초밥 수
        tmp_cnt = value[1]
        if key in tmp_sushi_names:  # 같은 위치에 사람과 초밥이 있는 경우
            name_idx = 0
            for i in range(len(sushi_name[idx])):
                if key == sushi_name[idx][i]:
                    name_idx = i
                    break
            tmp_sushi_cnt = tmp_sushi_cnts[name_idx]  # 있는 초밥 수
            # 초밥의 수가 더 많은 경우
            if tmp_cnt < tmp_sushi_cnt:
                sushi_cnt[idx][name_idx] -= tmp_cnt  # 초밥 상태만 변경
                ans_p -= 1  # 전체 사람 수 감소
                ans_s -= tmp_cnt  # 전체 초밥 수 감소
                # del people[key]  # 현재 사람 삭제
            # 먹어야할 수가 더 많은 경우
            elif tmp_cnt > tmp_sushi_cnt:
                value[1] -= tmp_sushi_cnt  # 사람 상태만 변경
                ans_s -= tmp_sushi_cnt  # 전체 초밥 수 감소
                del sushi_name[idx][name_idx]  # 현재 초밥 삭제
                del sushi_cnt[idx][name_idx]  # 현재 초밥 삭제
            # 같은 경우
            else:
                sushi_cnt[idx][name_idx] -= tmp_cnt  # 초밥 상태 변경
                value[1] -= tmp_cnt  # 사람 상태 변경
                ans_p -= 1  # 전체 사람 수 감소
                ans_s -= tmp_cnt  # 전체 초밥 수 감소
                # del people[key]  # 현재 사람 삭제
                del sushi_name[idx][name_idx]  # 현재 초밥 삭제
                del sushi_cnt[idx][name_idx]  # 현재 초밥 삭제

    keys = list(people.keys())
    for key in keys:
        if people[key][1] == 0:
            del people[key]

    print(ans_p, ans_s)

L, Q = map(int, input().split())
# sushi = [{} for i in range(L + 1)]
sushi_name = [[] for _ in range(L + 1)]  # 위치별 스시 이름 저장
sushi_cnt = [[] for _ in range(L + 1)]  # 위치별 스시 개수 저장
people = {}
ans_p = 0
ans_s = 0

for _ in range(Q):
    query = list(input().split())
    query[0] = int(query[0])
    if query[0] == 100:
        add_sushi(query)
        # print_sushi()
    elif query[0] == 200:
        add_person(query)
    elif query[0] == 300:
        photo(query)
    # print(query[1])
    # print_sushi()