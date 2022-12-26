# idea: regular maze search, but with time dimension too.
# make lookup func for map at time t

import numpy as np
import functools

with open("input", "r") as f:
    data = [l.strip() for l in f]

EMPTY = 0
WALL = 1
UP = 2
RIGHT = 3
DOWN = 4
LEFT = 5

default = np.zeros((len(data), len(data[0])), dtype=np.uint8) + EMPTY
winds: list[tuple[tuple[int, int], int]] = []
for i, l in enumerate(data):
    for j, char in enumerate(l):
        if char == "#":
            default[i, j] = WALL
        elif char == "<":
            winds.append(((i, j), LEFT))
        elif char == ">":
            winds.append(((i, j), RIGHT))
        elif char == "^":
            winds.append(((i, j), UP))
        elif char == "v":
            winds.append(((i, j), DOWN))

@functools.lru_cache
def get_state(t: int) -> np.ndarray:
    out = default.copy()
    for wind in winds:
        (y, x), dir = wind
        if dir == UP:
            y -= t
        elif dir == DOWN:
            y += t
        elif dir == LEFT:
            x -= t
        elif dir == RIGHT:
            x += t
        y = (y-1) % (default.shape[0] - 2) + 1
        x = (x-1) % (default.shape[1] - 2) + 1
        out[y, x] = WALL
    return out

explored = set()

# do a little maze solving
def shortest_road(start: tuple[int, int, int], end: tuple[int, int]):
    q = [start]
    while q:
        node = q.pop(0)
        if node in explored:
            continue
        explored.add(node)
        y, x, t = node
        if y >= default.shape[0]:
            continue
        if (y, x) == end:
            return t
        map = get_state(t)
        if map[y, x] == WALL:
            continue
        q.append((y - 1, x, t + 1))
        q.append((y + 1, x, t + 1))
        q.append((y, x + 1, t + 1))
        q.append((y, x - 1, t + 1))
        q.append((y, x, t + 1))
        
    else:
        return None

end = (default.shape[0] - 1, default.shape[1] - 2)
start = (0, 1)

t_end = shortest_road((*start, 0), end)
print(t_end)
explored.clear()
t_start = shortest_road((*end, t_end), start)
explored.clear()
print(shortest_road((*start, t_start), end))
