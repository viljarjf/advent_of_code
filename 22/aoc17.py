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

HEIGHT = 200
WIDTH = 7
cave = np.pad(np.zeros((HEIGHT, WIDTH)) + AIR, ((1, 0), (1, 1)), "constant", constant_values=WALL)

config_state = dict()

n = 0
blowstep = 0
height = 0
real_height = 0
target = 1000000000000
last_round = False

def nd_hash(arr: np.ndarray):
    return arr.tobytes()

while n < target:
    rock = get_rock(n)
    for i in range(len(rock)):
        rock[i][0] += height + 4        
        rock[i][1] += 2 + 1             # +1 for pad
    hit_ground = False
    while not hit_ground:
        # blow
        blowdir = 1 if blow[blowstep] == ">" else -1
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
        blowstep %= len(blow)
    for y, x in rock:
        cave[y, x] = ROCK
    n += 1

    # check if we can truncate the playfield
    check = np.count_nonzero(cave[1:, 1:-1] == ROCK, axis=0)
    if all(check > 0):        
        # need to find boundary. Do some simple colouring logic
        visited = set([(height + 7, i) for i in range(WIDTH + 2)])
        boundary_pos = []
        q = [(height + 6, 1)]
        while q:
            pos = q.pop() # bfs or dfs makes no difference
            if pos in visited:
                continue
            visited.add(pos)
            y, x = pos
            if cave[y, x] == AIR:
                q.append((y+1, x))
                q.append((y-1, x))
                q.append((y, x-1))
                q.append((y, x+1))
            else:
                boundary_pos.append(pos)
        boundary = [HEIGHT for _ in range(WIDTH + 2)]
        for y, x in boundary_pos:
            boundary[x-1] = min(boundary[x-1], y)
        boundary.pop()
        boundary.pop(0)

        new_bottom = min(boundary)
        new_top = height + 4
        cave[1:new_top, 1:-1] = cave[1 + new_bottom:new_top + new_bottom, 1:-1]

        real_height += new_bottom

    height = max(i - 1 if i < cave.shape[0] else 0 for i in (cave.shape[0] - np.argmax(cave[::-1, 1:-1] == ROCK, axis=0)))

    if not last_round:
        h = (nd_hash(cave), blowstep, n % N_ROCKS)
        if config_state.get(h) is not None:
            prev_n, prev_height = config_state[h]
            height_delta = (real_height + height) - prev_height
            n_delta = n - prev_n
            reps = (target - prev_n) // n_delta - 1
            n += n_delta * reps
            real_height += height_delta*reps
            last_round = True

        config_state[h] = (n, real_height + height)

height += real_height

print(height)