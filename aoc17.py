import numpy as np
from matplotlib import pyplot as plt

# y, x
N_ROCKS = 5
def get_rock(n: int) -> list[list[int, int]]:
    match n % N_ROCKS:
        case 0:
            return [[0, 0], [0, 1], [0, 2], [0, 3]]
        case 1:
            return [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]
        case 2:
            return [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
        case 3:
            return [[0, 0], [1, 0], [2, 0], [3, 0]]
        case 4:
            return [[0, 0], [0, 1], [1, 0], [1, 1]]

with open("input17.txt", "r") as f:
    blow = f.read().strip()

AIR = 0
ROCK = 1
WALL = -1

HEIGHT = 10000
WIDTH = 7
cave = np.pad(np.zeros((HEIGHT, WIDTH)) + AIR, ((1, 0), (1, 1)), "constant", constant_values=WALL)

n = 0
blowstep = 0
height = 0
real_height = 0
while n < 2022:
    rock = get_rock(n)
    for i in range(len(rock)):
        rock[i][0] += height + 4        
        rock[i][1] += 2 + 1             # +1 for pad
    hit_ground = False
    while not hit_ground:
        # blow
        blowdir = 1 if blow[blowstep % len(blow)] == ">" else -1
        for y, x in rock:
            if cave[y, x + blowdir] != AIR:
                break
        else:
            for i in range(len(rock)):
                rock[i][1] += blowdir
        # drop
        for y, x in rock:
            if cave[y - 1, x] != AIR:
                hit_ground = True
                break
        else:
            for i in range(len(rock)):
                rock[i][0] -= 1
        blowstep += 1
    for y, x in rock:
        cave[y, x] = ROCK
    height = max(max(r[0] for r in rock), height)
    n += 1

    ## This did not work...
    continue
    # check if we can truncate the playfield
    check = np.count_nonzero(cave[1:, 1:-1] == ROCK, axis = 0)
    if all(check):
        found = np.zeros((WIDTH), dtype=np.byte)
        i = height
        while not all(found):
            for j in range(WIDTH):
                if cave[i, j+1] == ROCK:
                    found[j] = 1
            i -= 1
        truncate_height_lower = i + 1
        truncate_height_upper = height
        dt = truncate_height_upper + 1 - truncate_height_lower
        cave[1:dt, 1:-1] = cave[truncate_height_lower + 1:truncate_height_upper + 1, 1:-1]
        cave[dt:truncate_height_upper + 1, 1:-1] = AIR
        real_height += height
        height = dt

height += real_height

# plt.imshow(cave[::-1, :][-height - 5:, :])
# plt.show()
    
print(height)