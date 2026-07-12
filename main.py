board =[[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
def render(board):
    for row in board:
        print(" ".join(f"{('.' if c == 0 else c):>4}" for c in row))
render(board)
