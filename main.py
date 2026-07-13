board =[[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
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
print(slide_left([2, 0, 2, 0]))  # [4,0,0,0]
print(slide_left([2, 2, 2, 0]))  # [4,2,0,0]
print(slide_left([2, 2, 2, 2]))  # [4,4,0,0]
print(slide_left([4, 4, 8, 0]))  # [8,8,0,0]
print(slide_left([0, 0, 0, 2]))  # [2,0,0,0]




