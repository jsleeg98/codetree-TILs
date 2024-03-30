import sys
import heapq

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline

empty_j = []  # 비어있는 채점기 j 저장 heap
work_j = []  # 채점 중인 j 채점기
work_d = {}  # 채점 중인 도메인
# wq = []  # 대기 큐 heap (p, t, u)
wq_d = {}  # 대기 큐 도메인 : 도메인별 heapq로 관리
wq_u = {}  # 대기 큐 url
hist_d = {}  # 채점 완료된 것 (도메인 : [])
ans = 0

# 채점 준비
def init(cnt_j, u):
    global empty_j, work_j, work_d, wq, wq_d, wq_u, ans
    empty_j = [i for i in range(1, cnt_j + 1)]
    work_j = [[] for i in range(0, cnt_j + 1)]
    work_d = {}
    # wq = []
    domain, id = u.split('/')
    wq_d = {domain: [(1, 0, u, domain, id)]}
    wq_u = {u: True}
    # wq.append((1, 0, u))
    ans += 1

# 채점 요청
def ask_check(t, p, u):
    global wq_u, ans
    # wq_d 일지 url 체크
    flag = wq_u.get(u, False)
    if not flag:
        wq_u[u] = True
        # heapq.heappush(wq, (p, t, u))
        # wq.append((p, t, u))
        domain, id = u.split('/')
        flag_d = wq_d.get(domain, False)
        if not flag_d:  # wq_d에 해당 도메인이 처음 들어오는 경우
            wq_d[domain] = [(p, t, u, domain, id)]
        else:  # 해당 도메인이 들어온적 있는 경우
            heapq.heappush(wq_d[domain], (p, t, u, domain, id))
        ans += 1

# 채점 시도
def try_check(t):  # 300
    global wq, work_d, wd_d, ans

    if len(empty_j) > 0:
        # 현재 채점 불가능한 도메인 검색
        can_d = []
        cannot_d = []
        for d in hist_d.keys():  # 채점 끝난 도메인 조건
            s, e, id, j_id = hist_d[d][-1]
            if t < s + 3 * (e - s):
                cannot_d.append(d)

        for d in work_d.keys():  # 채점 중인 도메인 채점 불가
            if work_d[d] == True:
                cannot_d.append(d)


        # wq_d에 있는 도메인 중 채점 가능한 도메인 내 최고 우선순위 요청 뽑기
        tmp = []
        for d in wq_d.keys():
            if len(wq_d[d]) > 0:
                if not d in cannot_d:
                    tmp.append(heapq.heappop(wq_d[d]))

        if len(tmp) > 0:  # 채점 가능한 요청이 있는 경우
            heapq.heapify(tmp)
            tmp_p, tmp_t, tmp_u, tmp_domain, tmp_id = heapq.heappop(tmp)  # 최고 우선 순위 뽑기
            # domain, id = tmp_u.split('/')
            work_d[tmp_domain] = True  # 채점 중인 도메인 처리
            wq_u[tmp_u] = False  # 채점 대기 큐의 url 제거 처리

            num_j = heapq.heappop(empty_j)  # 채점기 선정
            work_j[num_j] = (tmp_p, t, tmp_u, tmp_domain, tmp_id)  # 채점 중인 채점기 항목 추가
            ans -= 1
            if len(work_d[tmp_domain]) == 0:
                del work_d[tmp_domain]

            for i in range(len(tmp)):  # 채점 가능한 요청 중 채점 못한 것 다시 돌려놓기
                p, t, u, domain, id = tmp[i]
                # domain, id = u.split('/')
                heapq.heappush(wq_d[domain], (p, t, u, domain, id))




    # if len(empty_j) > 0:  # 쉬고 있는 채점기가 있는 경우
    #     # wq에서 우선순위대로 뽑기
    #     heapq.heapify(wq)
    #     wq_tmp = []
    #     while wq:
    #         tmp_p, tmp_t, tmp_u = heapq.heappop(wq)
    #         domain, id = tmp_u.split('/')
    #         flag_work = work_d.get(domain, False)
    #         if not flag_work:  # 현재 도메인이 채점 중이지 않은 경우
    #             flag_hist = hist_d.get(domain, False)
    #             if flag_hist:  # 채점 된 도메인인 경우
    #                 # 부적절 채점 확인
    #                 s, e, id, j_id = flag_hist[-1]
    #                 if t >= s + 3 * (e-s):  # 채점 가능 - 채점 시작
    #                     wq_d[tmp_u] = False  # 대기 큐 도메인 False 변환
    #                     work_d[domain] = True  # 채점 중 도메인 True 변경
    #                     # heapq.heapify(empty_j)  # 비어있는 채점기 중 가장 작은 번호 얻기
    #                     # num_j = empty_j[0]
    #                     num_j = heapq.heappop(empty_j)
    #                     work_j[num_j] = (tmp_p, t, tmp_u)  # 채점기에 추가
    #                     # if len(wq_tmp) > 0:
    #                     #     for tmp in wq_tmp:
    #                     #         heapq.heappush(wq, tmp)
    #                     #         # wq.append(tmp)  # 불가능했던 것들 다시 wq에 추가
    #                     break
    #                 else:
    #                     # heapq.heappush(wq_tmp, (tmp_p, tmp_t, tmp_u))
    #                     wq_tmp.append((tmp_p, tmp_t, tmp_u))  # 불가능 리스트 추가
    #             else:  # 한번도 채점 안된 도메인인 경우 - 채점 시작
    #                 wq_d[tmp_u] = False  # 대기 큐 도메인 False 변환
    #                 work_d[domain] = True  # 채점 중 도메인 True 변경
    #                 # heapq.heapify(empty_j)  # 비어있는 채점기 중 가장 작은 번호 얻기
    #                 # num_j = empty_j[0]
    #                 num_j = heapq.heappop(empty_j)
    #                 work_j[num_j] = (tmp_p, t, tmp_u)  # 채점기에 추가
    #                 # if len(wq_tmp) > 0:
    #                 #     for tmp in wq_tmp:
    #                 #         heapq.heappush(wq, tmp)
    #                 #         # wq.append(tmp)  # 불가능했던 것들 다시 wq에 추가
    #                 break
    #         else:  # 현재 도메인이 채점 중인 경우
    #             # heapq.heappush(wq_tmp, (tmp_p, tmp_t, tmp_u))
    #             wq_tmp.append((tmp_p, tmp_t, tmp_u))  # 불가능 리스트 추가
    #     # if len(wq_tmp) > 0:
    #     #     for tmp in wq_tmp:
    #     #         # heapq.heappush(wq, tmp)
    #     #         wq.append(tmp)  # 불가능했던 것들 다시 wq에 추가
    #     if len(wq_tmp) > 0:
    #         # for tmp in wq_tmp:
    #         #     heapq.heappush(wq, tmp)
    #         wq += wq_tmp

# 채점 종료
def end_check(t, j_id):
    global work_j, work_d, empty_j, hist_d
    if len(work_j[j_id]) > 0:
        tmp_p, tmp_t, tmp_u, tmp_domain, tmp_id = work_j[j_id]
        work_j[j_id] = []  # 채점기 종료
        # domain, id = tmp_u.split('/')
        flag = hist_d.get(tmp_domain, False)  # 완료 도메인 존재 학인
        if not flag:  # 없으면
            hist_d[tmp_domain] = [(tmp_t, t, id, j_id)]  # 새로 추가
        else:
            hist_d[tmp_domain].append((tmp_t, t, id, j_id))  # 채점 끝난 기록 append
        # work_d[tmp_domain] = False  # 채점 중이 아님 표시
        work_d.pop(tmp_domain)  # 채점 중이 아님 표시
        heapq.heappush(empty_j, j_id)  # 남은 채점기에 추가
        # empty_j.append(j_id)  # 비어있는 채점기에 추가

# 채점 대기 큐 조회
def check_wq(t):
    # print(len(wq))
    # cnt = 0
    # for d, ds in wq_d.items():
    #     cnt += len(ds)

    print(ans)

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