from game import *
import random

def legal_moves(board):
    moves = []
    for move in (move_up, move_down, move_left, move_right):
        if move(board) != board:
            moves.append(move)
    return moves




WEIGHTS = [[ 1,  2,  4,  8],
           [ 2,  4,  8, 16],
           [ 4,  8, 16, 32],
           [ 8, 16, 32, 64]]

def score(board):
    empties = sum(1 for row in board for c in row if c == 0)
    positional = sum(board[r][c] * WEIGHTS[r][c] for r in range(4) for c in range(4))
    return empties * 100 + positional


def copy_board(board):
    return [row[:] for row in board]


def expectimax(board, depth, is_max):
    if depth == 0 or is_game_over(board):
        return score(board)

    if is_max:
        best = float('-inf')
        for move in legal_moves(board):
            value = expectimax(move(board), depth - 1, False)
            best = max(best, value)
        return best

    else:
        empties = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
        if not empties:
            return score(board)

        total = 0
        for (r, c) in empties:
            for value, prob in ((2, 0.9), (4, 0.1)):
                new_board = copy_board(board)
                new_board[r][c] = value
                p = prob / len(empties)
                total += p * expectimax(new_board, depth - 1, True)
        return total


def best_move(board, depth=4):
    best_value = float('-inf')
    chosen = None
    for move in legal_moves(board):
        value = expectimax(move(board), depth - 1, False)
        if value > best_value:
            best_value = value
            chosen = move
    return chosen

def run_bot(show=True):
    board = [[0]*4 for _ in range(4)]
    spawn(board); spawn(board)
    while True:
        if show:
            render(board)
        if is_game_over(board):
            break
        move = best_move(board)
        board = move(board)
        spawn(board)
    return max(max(row) for row in board)


def benchmark(n=20):
    results = [run_bot(show=False) for _ in range(n)]
    wins = sum(1 for r in results if r >= 2048)
    print(f"games: {n}")
    print(f"reached 2048: {wins}/{n}")
    print(f"best tile: {max(results)}")
    print(f"worst tile: {min(results)}")
    print(f"all: {sorted(results, reverse=True)}")

benchmark(100)