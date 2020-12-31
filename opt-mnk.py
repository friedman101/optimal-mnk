#!/usr/bin/python3

from copy import deepcopy
from numpy import argmax, argmin
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

    # right
    if j + k <= m:
        for j_next in range(j+1,j+k):
            if board[i][j] != board[i][j_next]:
                break
        else:
            return True, board[i][j]

    # down
    if i + k <= n:
        for i_next in range(i+1,i+k):
            if board[i][j] != board[i_next][j]:
                break
        else:
            return True, board[i][j]

    # down-right
    if i + k <= n and j + k <= m:
        for inc in range(1,k):
            if board[i][j] != board[i+inc][j+inc]:
                break
        else:
            return True, board[i][j]

    # down-left
    if i + k <= n and j - k >= -1:
        for inc in range(1,k):
            if board[i][j] != board[i+inc][j-inc]:
                break
        else:
            return True, board[i][j]

    return  False, 0


def iswinloss(board, me, k):
    m = len(board[0])
    n = len(board)

    for i in range(n):
        for j in range(m):
            hit, winner = kinarow(board, i, j, k)
            if hit and winner == me:
                return 1
            if hit and winner != me:
                return -1

    return 0

def tuple_replace(data,i,j,rep):
    out = [[x for x in row] for row in data]
    out[i][j] = rep
    for i in range(len(out)):
        out[i] = tuple(out[i])
    return tuple(out)


@lru_cache(maxsize=None)
def minimax(board, me, turn, style, k):
    m = len(board[0])
    n = len(board)

    winloss = style*iswinloss(board, me, k)
    if winloss != 0:
        return winloss/turns(board), 0
    outcomes = []
    moves = []
    
    full = True
    next_turn = 2 if turn == 1 else 1
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                full = False
                #next_board = deepcopy(board)
                #next_board[i][j] = turn
                next_board = tuple_replace(board,i,j,turn)
                outcome, move = minimax(next_board, me, next_turn, style, k)
                outcomes += [outcome]
                moves += [[i,j]]

    if full:
        return 0,0
    
    if me == turn:
        idx = argmax(outcomes)
    else:
        idx = argmin(outcomes)
    return outcomes[idx], moves[idx]


def print_board(board):
    m = len(board[0])
    n = len(board)

    for i in range(n):
        for j in range(m):
            cell = board[i][j]
            if cell == 0:
                print('%2i ' % (i*3+j),end='')
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
parser.add_argument('m', help='Board columns')
parser.add_argument('n', help='Board rows')
parser.add_argument('k', help='K in a row to win')
parser.add_argument('style', help='Style, 1 for normal, -1 for misère')
args = parser.parse_args()

m = int(args.m)
n = int(args.m)
k = int(args.k)
style = int(args.style)

board = tuple([tuple([0 for i in range(m)]) for j in range(n)])

print_board(board)

turn = 1
while(True):
    outcome, move = minimax(board,turn,turn,style,k)    
    if move == 0:
        winloss = iswinloss(board, 1, k)
        if winloss == 1:
            print('Player 1 wins')
        elif winloss == -1:
            print('Player 2 wins')
        else:
            print('Tie')
        exit()
    board = tuple_replace(board, move[0], move[1], turn)
    print_board(board)
    turn = 2 if turn == 1 else 1
