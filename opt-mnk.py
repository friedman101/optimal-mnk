#!/usr/bin/python3

from copy import deepcopy
from functools import lru_cache
import argparse

def idx2(data2, idx):
    return data2[idx[0]][idx[1]]

def turns(board):
    return sum([1 if cell != 0 else 0 for row in board for cell in row])

def kinarow(board, i, j, k):
    if board[i][j] == 0:
        return False, 0

    m = len(board[0])
    n = len(board)

    dirs = (  (0,1), (1,0), (1,1), (1,-1) )
    for dir in dirs:
        i_max = i+(k-1)*dir[0]
        if i_max >= n or i_max < 0:
            continue
        j_max = j+(k-1)*dir[1]
        if j_max >= m or j_max < 0:
            continue

        for inc in range(1,k):
            i_next = i+inc*dir[0]
            j_next = j+inc*dir[1]
            if board[i][j] != board[i_next][j_next]:
                break
        else:
            return True, board[i][j]

    return False, 0

def iswinloss(board, me, k, style):
    m = len(board[0])
    n = len(board)

    for i in range(n):
        for j in range(m):
            hit, winner = kinarow(board, i, j, k)
            if hit and winner == me:
                return 1*style
            if hit and winner != me:
                return -1*style

    return 0

def tuple_replace(data,i,j,rep):
    out = list(deepcopy(data))
    out[i] = list(out[i])
    out[i][j] = rep
    out[i] = tuple(out[i])
    return tuple(out)


@lru_cache(maxsize=None)
def minimax(board, me, style, k):
    m = len(board[0])
    n = len(board)

    winloss = iswinloss(board, me, k, style)
    if winloss != 0:
        return winloss/turns(board), 0
    
    best_outcome = 0
    best_move = [0,0]
    first = True
    
    full = True
    next_me = 2 if me == 1 else 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                full = False
                next_board = tuple_replace(board,i,j,me)
                outcome, move = minimax(next_board, next_me, style, k)
                outcome *= -1
                if first or outcome > best_outcome:
                    first = False
                    best_outcome = outcome
                    best_move = [i,j]

    if full:
        return 0,0

    return best_outcome, best_move

def get_human_move(m):
    move_number = int(input('Move: '))
    move = divmod(move_number, m)
    return move

def print_board(board, show_move_number=False):
    m = len(board[0])
    n = len(board)

    for i in range(n):
        for j in range(m):
            cell = board[i][j]
            if cell == 0:
                if show_move_number:
                    print('%2i ' % (i*m+j),end='')
                else:
                    print('   ',end='')
            elif cell == 1:
                print(' X ',end='')
            else:
                print(' O ',end='')
            if j != m-1:
                print('|',end='')
            else:
                print()
        if i != n-1:
            print('----'*m)
    print()

parser = argparse.ArgumentParser(description='Play optimal m,n,k-game. Arguments 3 3 3 1 plays tic-tac-toe')
parser.add_argument('m', help='Board columns', type=int)
parser.add_argument('n', help='Board rows', type=int)
parser.add_argument('k', help='K in a row to win', type=int)
parser.add_argument('style', help='Style, 1 for normal, -1 for misère', type=int)
parser.add_argument('--play-first', help='flag to let human play first', action="store_true")
parser.add_argument('--play-second', help='flag to let human play second', action="store_true")
args = parser.parse_args()

m = args.m
n = args.n
k = args.k
style = args.style

board = tuple([tuple([0 for i in range(m)]) for j in range(n)])

turn = 1
turn_cnt = [0,0]
comp_vs_comp = not args.play_first and not args.play_second
full = False
winloss = 0

print_board(board, not comp_vs_comp)
while(not full and winloss == 0):
    odd_turn = sum(turn_cnt)%2
    if not odd_turn and args.play_first:
        move = get_human_move(m)
    elif odd_turn and args.play_second:
        move = get_human_move(m)
    else:
        outcome, move = minimax(board,turn,style,k)    
    board = tuple_replace(board, move[0], move[1], turn)
    turn_cnt[turn-1]+=1
    print_board(board, not comp_vs_comp)

    full = turns(board) == m*n
    winloss = iswinloss(board, 1, k, style)
    if winloss > 0:
        print('Player 1 wins in %i turns' % turn_cnt[0])
    elif winloss < 0:
        print('Player 2 wins in %i turns' % turn_cnt[1])
    elif full:
        print('Draw')

    turn = 2 if turn == 1 else 1

