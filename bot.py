from game import *
import random

def legal_moves(board):
    moves = []
    for move in (move_up, move_down, move_left, move_right):
        if move(board) != board:
            moves.append(move)
    return moves

def run_bot():
    board = [[0]*4 for _ in range(4)]
    spawn(board); spawn(board)
    while True:
        render(board)
        if is_game_over(board):
            break
        move = random.choice(legal_moves(board))
        board = move(board)       # apply the chosen move
        spawn(board)                # add a new tile

run_bot()