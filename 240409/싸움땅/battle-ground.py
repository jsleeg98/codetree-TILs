import sys
import heapq

# sys.stdin = open('input.txt', 'r')

input = sys.stdin.readline

class Player:
    def __init__(self, r, c, d, s):
        self.r = r
        self.c = c
        self.d = d
        self.s = s
        self.gun = 0
        self.score = 0



def get_gun(player):
    global board
    cr, cc = player.r, player.c
    # 해당 위치에 총이 있는 경우
    if len(board[cr][cc]) > 0:
        # 가장 공격력이 높은 총 꺼내기
        tmp_gun = -board[cr][cc][0]
        # 해당 플레이어가 총을 가지고 있는 경우 : 바꾸기
        if player.gun != 0:
            # 총을 바꿔야하는 경우
            if player.gun < tmp_gun:
                heapq.heappop(board[cr][cc])
                tmp_player_gun = player.gun  # 플레이어 총 임시 저장
                player.gun = tmp_gun  # 총 바꾸기
                heapq.heappush(board[cr][cc], -tmp_player_gun)  # 총 버리기
        # 총이 없는 경우 줍기만 하기
        else:
            heapq.heappop(board[cr][cc])
            player.gun = tmp_gun

def fight(player_1, player_2, cr, cc):
    global players, board, player_board
    # 점수 계산
    player_1_score = players[player_1].s + players[player_1].gun
    player_2_score = players[player_2].s + players[player_2].gun

    winner_idx = -1
    loser_idx = -1

    # 1번 플레이어가 이긴 경우
    if player_1_score > player_2_score:
        winner_idx = player_1
        loser_idx = player_2
    elif player_1_score == player_2_score:
        # 1번 플레이어가 이긴 경우
        if players[player_1].s > players[player_2].s:
            winner_idx = player_1
            loser_idx = player_2
        # 2번 플레이어가 이긴 경우
        else:
            winner_idx = player_2
            loser_idx = player_1
    # 2번 플레이어가 이긴 경우
    else:
        winner_idx = player_2
        loser_idx = player_1

    # 이긴 플레이어 포인트 획득
    players[winner_idx].score += abs(player_1_score - player_2_score)
    # 이긴 플레이어 위치 변경
    players[winner_idx].r = cr
    players[winner_idx].c = cc

    # 진 플레이어 총 내려놓기
    if players[loser_idx].gun > 0:
        tmp_gun = players[loser_idx].gun
        players[loser_idx].gun = 0
        heapq.heappush(board[cr][cc], -tmp_gun)



    # 진 플레이어 이동
    for i in range(players[loser_idx].d, players[loser_idx].d + 4):
        d = i % 4
        nr = cr + dir[d][0]
        nc = cc + dir[d][1]
        # 격자 밖인 경우 패스
        if 1 > nr or n < nr or 1 > nc or n < nc:
            continue
        # 다른 플레이어 있는 경우 패스
        if player_board[nr][nc] != -1:
            continue
        players[loser_idx].r = nr  # 진 플레이어 위치 변경
        players[loser_idx].c = nc
        players[loser_idx].d = d  # 진 플레이어 방향 변경
        break

    # 진 플레이어 총 줍기
    get_gun(players[loser_idx])

    # 이긴 플레이어 총 줍기
    get_gun(players[winner_idx])

    # 위치 조정
    player_board[players[winner_idx].r][players[winner_idx].c] = winner_idx
    player_board[players[loser_idx].r][players[loser_idx].c] = loser_idx

def print_player_board():
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            print(f'{player_board[r][c]:<3}', end=' ')
        print()
    print('-' * 20)

def print_player():
    for i in range(1, m + 1):
        print(f'{i} score : {players[i].score}')
        print(f'{i} gun : {players[i].gun}')

n, m, k = map(int, input().split())

board = [[[] for _ in range(n + 1)] for _ in range(n + 1)]  # 총과 빈칸 배열, 힙으로 구성
players = [[]]
dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

for r in range(1, n + 1):
    tmp = list(map(int, input().split()))
    for c in range(0, n):
        if tmp[c] > 0:
            board[r][c + 1].append(-tmp[c])

for _ in range(m):
    r, c, d, s = map(int, input().split())
    players.append(Player(r, c, d, s))

for _ in range(k):
    # 플레이어가 있는 위치 표시
    player_board = [[-1 for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(1, m + 1):
        r, c = players[i].r, players[i].c
        player_board[r][c] = i
    # print_player_board()
    for i in range(1, m + 1):
        # 플레이어 이동
        cr, cc, cd = players[i].r, players[i].c, players[i].d
        player_board[cr][cc] = -1  # 기존 위치 제거
        nr = cr + dir[cd][0]
        nc = cc + dir[cd][1]
        # 벗어나지 않는 경우
        if 0 < nr < n + 1 and 0 < nc < n + 1:
            # 플레이어 위치 갱신
            players[i].r = nr
            players[i].c = nc
        # 벗어나는 경우 반대로 이동
        else:
            cd = (cd + 2) % 4  # 방향 반대 전환
            nr = cr + dir[cd][0]
            nc = cc + dir[cd][1]
            players[i].d = cd  # 플레이어 방향 갱신
            # 플레이어 위치 갱신
            players[i].r = nr
            players[i].c = nc
        # 플레이어가 없는 경우 : 총 줍기
        cr, cc = players[i].r, players[i].c
        if player_board[cr][cc] == -1:
            get_gun(players[i])
            player_board[cr][cc] = i
        # 플레이어가 있는 경우 : 싸움
        else:
            fight(i, player_board[cr][cc], cr, cc)
    # print_player_board()
    # print_player()

for i in range(1, m + 1):
    print(players[i].score, end=' ')