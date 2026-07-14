import random
board =[[2,0,0,0],
        [2,0,0,0],
        [4,0,0,0],
        [4,0,0,0]]
def render(board):
    for row in board:
        print(" ".join(f"{('.' if c == 0 else c):>4}" for c in row))
render(board)
def slide_left(row):
    tiles = [c for c in row if c != 0]
    merged = []
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged.append(tiles[i]*2)
            i += 2
        else:
            merged.append(tiles[i])
            i+=1
    return merged + [0] * (4 - len(merged))

def slide_right(row):
    return slide_left(row[::-1])[::-1]

def transpose(board):
    return [[board[r][c] for r in range(4)] for c in range(4)]

def move_up(board):
    t = transpose(board)
    t = [slide_left(row) for row in t]     # slide each row left
    return transpose(t)


def move_down(board):
    t = transpose(board)
    t = [slide_right(row) for row in t]     # slide each row left
    return transpose(t)

def spawn(board):
    empties = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if not empties:
        return
    r, c = random.choice(empties)
    value = 2 if random.random() < 0.9 else 4
    board[r][c] = value

b = [[0]*4 for _ in range(4)]
spawn(b)
spawn(b)
render(b)

def move_left(board):
    return [slide_left(row) for row in board]

def move_right(board):
    return [slide_right(row) for row in board]

=def is_game_over(board):
    if move_up(board) == board and move_down(board) == board \
       and move_left(board) == board and move_right(board) == board:
        return True
    return False