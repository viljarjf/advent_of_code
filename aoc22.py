import numpy as np
from matplotlib import pyplot as plt

row_lims = []
x_max = 0
y_max = 0

walls = dict()

with open("input22.txt", "r") as f:
    content = f.read().split("\n")[:-1]
    moves = content.pop()

    for i, line in enumerate(content):
        if not line:
            break
        y_max += 1
        row_min = min(line.index("."), float("inf") if "#" not in line else line.index("#"))
        row_delta = len(line) - row_min
        row_lims.append((row_min, row_delta))
        for j in range(len(line)):
            if line[j] == "#":
                walls[(i, j)] = 1
        x_max = max(x_max, len(line))        
TILEWIDTH = x_max // 3
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

moves = moves.replace("R", ",R,").replace("L", ",L,").split(",")
for move in moves:
    if move.isnumeric():
        for _ in range(int(move)):
            x_min, x_delta = row_lims[pos[0]]
            y_min, y_delta = col_lims[pos[1]]
            pos += movedir
            # boundary
            if pos[0] < y_min or pos[0] >= y_min + y_delta:
                pos[0] = (pos[0] - y_min) % y_delta + y_min
            if pos[1] < x_min or pos[1] >= x_min + x_delta:
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
        
# plt.imshow(test)
# plt.show()

print(movedir)
print(1000*(pos[0] + 1) + 4*(pos[1] + 1))


# I made a cardboard cutout to figure out 
# the traversal and orientations.
# I will hard-code a lot of this

#   1 2
#   3  
# 4 5  
# 6    

# these are the neighbours with orientation.
# +: rotate anticlockwise
# -: rotate clockwise
# ^: rotate twice
# +---------+---------+---------+
# |    6+   |    6    |    1    |
# | 4^ 1 2  | 1  2 5^ | 4- 3 2- |
# |    3    |    3+   |    5    |
# +---------+---------+---------+
# |    3+   |    3    |    4    |
# | 1^ 4 5  | 4  5 2^ | 1- 6 5- |
# |    6    |    6+   |    2    |
# +---------+---------+---------+

# Relevant transitions:
# +---------+---------+---------+
# |    6+   |    6    |         |
# | 4^ 1    |    2 5^ | 4- 3 2- |
# |         |    3+   |         |
# +---------+---------+---------+
# |    3+   |         |         |
# | 1^ 4    |    5 2^ | 1- 6 5- |
# |         |    6+   |    2    |
# +---------+---------+---------+

def get_side(pos: tuple[int, int]) -> int | None:
    y, x = pos
    y //= TILEWIDTH
    x //= TILEWIDTH
    match (y, x):
        case (0, 1):
            return 1
        case (0, 2):
            return 2
        case (1, 1):
            return 3
        case (2, 0):
            return 4
        case (2, 1):
            return 5
        case (3, 0):
            return 6
    return None

def get_pos(side: int) -> tuple[int, int]:
    return [ None,
        (0 * TILEWIDTH, 1 * TILEWIDTH),
        (0 * TILEWIDTH, 2 * TILEWIDTH),
        (1 * TILEWIDTH, 1 * TILEWIDTH),
        (2 * TILEWIDTH, 0 * TILEWIDTH),
        (2 * TILEWIDTH, 1 * TILEWIDTH),
        (3 * TILEWIDTH, 0 * TILEWIDTH),
    ][side]

def transition(pos: np.ndarray, dir: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """return new pos, new dir"""
    pos -= dir
    dir = (dir[0], dir[1])
    DOWN    = ( 1,  0)
    UP      = (-1,  0)
    LEFT    = ( 0, -1)
    RIGHT   = ( 0,  1)
    s = get_side(pos)
    match s:
        case 1 | 4:
            if dir == UP:
                y, x = get_pos(6 if s == 1 else 3)
                y += pos[1] % TILEWIDTH
                return np.array([y, x]), np.array(RIGHT)
            elif dir == LEFT:
                y, x = get_pos(4 if s == 1 else 1)
                y += TILEWIDTH - 1 - pos[0] % TILEWIDTH
                return np.array([y, x]), np.array(RIGHT)
        case 2 | 5:
            if dir == RIGHT:
                y, x = get_pos(5 if s == 2 else 2)
                x += TILEWIDTH - 1
                y += TILEWIDTH - 1 - pos[0] % TILEWIDTH
                return np.array([y, x]), np.array(LEFT)
            elif dir == DOWN:
                y, x = get_pos(3 if s == 2 else 6)
                x += TILEWIDTH - 1
                y += pos[1] % TILEWIDTH
                return np.array([y, x]), np.array(LEFT)
            elif dir == UP:
                # only matches on 2
                y, x = get_pos(6)
                x += pos[1] % TILEWIDTH
                y += TILEWIDTH - 1
                return np.array([y, x]), np.array(UP)
        case 3 | 6:
            if dir == LEFT:
                y, x = get_pos(4 if s == 3 else 1)
                x += pos[0] % TILEWIDTH
                return np.array([y, x]), np.array(DOWN)
            elif dir == RIGHT:
                y, x = get_pos(2 if s == 3 else 5)
                x += pos[0] % TILEWIDTH
                y += TILEWIDTH - 1
                return np.array([y, x]), np.array(UP)
            elif dir == DOWN:
                # only matches on 6
                y, x = get_pos(2)
                x += pos[1] % TILEWIDTH
                return np.array([y, x]), np.array(DOWN)
    return None, None

test2 = np.zeros((y_max, x_max), dtype=np.byte) + ILLEGAL
for x, (mi, d) in enumerate(col_lims):
    test2[mi:mi+d, x] = LEGAL

for key in walls.keys():
    test2[key] = WALL

pos = np.array([0, row_lims[0][0]])
# pos = np.array([148, 98])
movedir = np.array([0, 1])

for move in moves:
    if move.isnumeric():
        for _ in range(int(move)):
            x_min, x_delta = row_lims[pos[0]]
            y_min, y_delta = col_lims[pos[1]]
            pos += movedir
            # boundary
            if pos[0] < y_min or pos[0] >= y_min + y_delta:
                pos, movedir = transition(pos, movedir)
            elif pos[1] < x_min or pos[1] >= x_min + x_delta:
                pos, movedir = transition(pos, movedir)
            # check if we crash
            if walls.get(tuple(pos)) is not None:
                pos -= movedir
                pos[0] = (pos[0] - y_min) % y_delta + y_min
                pos[1] = (pos[1] - x_min) % x_delta + x_min
            test2[pos[0], pos[1]] = POS
    
    else:
        if move == "R":
            movedir = np.array([movedir[1], -movedir[0]])
        elif move == "L":
            movedir = np.array([-movedir[1], movedir[0]])
        else:
            print(move)
        
plt.imshow(test2)
plt.show()

print(movedir)
print(1000*(pos[0] + 1) + 4*(pos[1] + 1))