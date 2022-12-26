import numpy as np
from matplotlib import pyplot as plt

row_lims = []
x_max = 0
y_max = 0

walls = dict()

with open("input", "r") as f:
    content = f.read().split("\n")[:-1]
    moves = content.pop()

    for i, line in enumerate(content):
        if not line:
            break
        y_max += 1
        row_min = min(line.index("."), line.index("#"))
        row_delta = len(line) - row_min
        row_lims.append((row_min, row_delta))
        for j in range(len(line)):
            if line[j] == "#":
                walls[(i, j)] = 1
        x_max = max(x_max, len(line))        

# recreate
POS = 4
VISITED = 3
WALL = 2
LEGAL = 1
ILLEGAL = 0
test = np.zeros((y_max, x_max), dtype=np.byte) + ILLEGAL
for y, (mi, d) in enumerate(row_lims):
    test[y, mi:mi+d] = LEGAL

for key in walls.keys():
    test[key] = WALL

# use 2d arr to find column limits
col_lims = []
for i in range(test.shape[1]):
    col = test[:, i]
    col_ind = np.argwhere(col != ILLEGAL)
    col_min = np.min(col_ind)
    col_max = np.max(col_ind)
    col_delta = col_max - col_min
    col_lims.append((col_min, col_delta + 1))


pos = np.array([0, row_lims[0][0]])
movedir = np.array([0, 1])

move = ""
moves = moves.replace("R", ",R,").replace("L", ",L,").split(",")
for move in moves:
    if move.isnumeric():
        for _ in range(int(move)):
            x_min, x_delta = row_lims[pos[0]]
            y_min, y_delta = col_lims[pos[1]]
            pos += movedir
            # boundary
            pos[0] = (pos[0] - y_min) % y_delta + y_min
            pos[1] = (pos[1] - x_min) % x_delta + x_min
            # check if we crash
            if walls.get(tuple(pos)) is not None:
                pos -= movedir
                pos[0] = (pos[0] - y_min) % y_delta + y_min
                pos[1] = (pos[1] - x_min) % x_delta + x_min
            test[pos[0], pos[1]] = POS
    
    else:
        if move == "R":
            movedir = np.array([movedir[1], -movedir[0]])
        elif move == "L":
            movedir = np.array([-movedir[1], movedir[0]])
        else:
            print(move)
        
plt.imshow(test)
plt.show()

print(movedir)
print(1000*(pos[0] + 1) + 4*(pos[1] + 1))

#   1 2
#   3  
# 4 5  
# 6    
