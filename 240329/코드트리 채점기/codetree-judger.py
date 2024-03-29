import sys
import heapq

input = sys.stdin.readline

empty_j = []  # 비어있는 j 저장 heap
work_j = []  # 채점 중인 j
work_d = {}  # 채점 중인 도메인
wq = []  # 대기 큐 heap (p, t, u)
wq_d = {}  # 대기 큐 도메인
hist_d = {}  # 채점 완료된 것 (도메인 : [])

# 채점 준비
def init(cnt_j, u):
    global empty_j, work_j, work_d, wq, wq_d
    empty_j = [i for i in range(1, cnt_j + 1)]
    work_j = [[] for i in range(0, cnt_j + 1)]
    work_d = {}
    wq = []
    wq_d = {u: True}
    wq.append((1, 0, u))

# 채점 요청
def ask_check(t, p, u):
    global wq_d
    # wq_d 일지 url 체크
    flag = wq_d.get(u, False)
    if not flag:
        wq_d[u] = True
        wq.append((p, t, u))

# 채점 시도
def try_check(t):
    global wq, work_d
    if len(empty_j) > 0:  # 쉬고 있는 채점기가 있는 경우
        # wq에서 우선순위대로 뽑기
        heapq.heapify(wq)
        wq_tmp = []
        while wq:
            tmp_p, tmp_t, tmp_u = heapq.heappop(wq)
            domain, id = tmp_u.split('/')
            flag_work = work_d.get(domain, False)
            if not flag_work:  # 현재 도메인이 채점 중이지 않은 경우
                flag_hist = hist_d.get(domain, False)
                if flag_hist:  # 채점 된 도메인인 경우
                    # 부적절 채점 확인
                    s, e, id, j_id = flag_hist[-1]
                    if t >= s + 3 * (e-s):  # 채점 가능
                        wq_d[tmp_u] = False  # 채점 큐 도메인 False 변환
                        work_d[domain] = True  # 채점 중 도메인 True 변경
                        heapq.heapify(empty_j)  # 비어있는 채점기 중 가장 작은 번호 얻기
                        num_j = empty_j[0]
                        work_j[num_j] = (tmp_p, t, tmp_u)  # 채점기에 추가
                        if len(wq_tmp) > 0:
                            wq.append(*wq_tmp)  # 불가능했던 것들 다시 wq에 추가
                        break
                    else:
                        wq_tmp.append((tmp_p, tmp_t, tmp_u))  # 불가능 리스트 추가
                else:  # 한번도 채점 안된 도메인인 경우 - 채점 시작
                    work_d[domain] = True  # 채점 중 도메인 True 변경
                    heapq.heapify(empty_j)  # 비어있는 채점기 중 가장 작은 번호 얻기
                    num_j = empty_j[0]
                    work_j[num_j] = (tmp_p, t, tmp_u)  # 채점기에 추가
                    if len(wq_tmp) > 0:
                        wq.append(*wq_tmp)  # 불가능했던 것들 다시 wq에 추가
                    break
            else:  # 현재 도메인이 채점 중인 경우
                wq_tmp.append((tmp_p, tmp_t, tmp_u))  # 불가능 리스트 추가
        if len(wq_tmp) > 0:
            wq.append(*wq_tmp)  # 불가능했던 것들 다시 wq에 추가

# 채점 종료
def end_check(t, j_id):
    global work_j, work_d, empty_j, hist_d
    if len(work_j[j_id]) > 0:
        tmp_p, tmp_t, tmp_u = work_j[j_id]
        work_j[j_id] = []
        domain, id = tmp_u.split('/')
        flag = hist_d.get(domain, False)
        if not flag:
            hist_d[domain] = [(tmp_t, t, id, j_id)]
        else:
            hist_d[domain].append((tmp_t, t, id, j_id))  # 채점 끝난 기록
        work_d[domain] = False  # 채점 중이 아님 표시
        empty_j.append(j_id)  # 비어있는 채점기에 추가

# 채점 대기 큐 조회
def check_wq(t):
    print(len(wq))


Q = int(input())
for _ in range(Q):
    cmd = input().split()
    if cmd[0] == '100':  # 채점 준비
        init(int(cmd[1]), cmd[2])
    elif cmd[0] == '200':  # 채점 요청
        ask_check(int(cmd[1]), int(cmd[2]), cmd[3])
    elif cmd[0] == '300':  # 채점 시도
        try_check(int(cmd[1]))
    elif cmd[0] == '400':  # 채점 종료
        end_check(int(cmd[1]), int(cmd[2]))
    elif cmd[0] == '500':  # 채점 대기 큐 조회
        check_wq(int(cmd[1]))