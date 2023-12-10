import numpy as np
from matplotlib import pyplot as plt

tiles = {
    ".": np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]),
    "|": np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]),
    "-": np.array([
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]),
    "L": np.array([
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]),
    "J": np.array([
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]),
    "7": np.array([
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
    ]),
    "F": np.array([
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]),
    "S": np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]),
}

def main():
    pipes = []
    keys = []
    with open("10", "r", encoding="utf-8") as inp:
        for line in inp:
            pipe_line = []
            key_line = []
            for tile in line.strip():
                pipe_line.append(tiles[tile])
                key_line.append(tile)
            pipes.append(pipe_line)
            keys.append(key_line)

    pipes = np.block(pipes)
    keys = np.array(keys)

    start = np.where(keys == "S")
    start = (3 * start[0] + 1, 3 * start[1] + 1)
    pipes[start] = 2

    plt.figure()
    plt.imshow(pipes)
    plt.show()

    # BFS
    dists = np.zeros_like(pipes, dtype=int) - 1
    to_search = [(start, 0)]
    ymax, xmax = dists.shape
    ymax -= 1
    xmax -= 1
    while to_search:
        pos, dist = to_search.pop(0)
        if pipes[pos] == 0:
            continue
        if dists[pos] >= 0:
            continue
        dists[pos] = dist
        y, x = pos
        to_search += [
            (
                (
                    max(min(y + 1, ymax), 0), 
                    x,
                ), 
                dist + 1,
            ),
            (
                (
                    max(min(y - 1, ymax), 0), 
                    x,
                ), 
                dist + 1,
            ),
            (
                (
                    y,
                    max(min(x + 1, xmax), 0), 
                ), 
                dist + 1,
            ),
            (
                (
                    y,
                    max(min(x - 1, xmax), 0), 
                ), 
                dist + 1,
            ),
        ]

    plt.figure()
    plt.imshow(dists)
    plt.show()

    print("Max distance:", np.max(dists) // 3)

    # Find the enclosed region
    explored = np.zeros_like(pipes, dtype=bool)
    explored[pipes != 0] = True
    TL = (start[0] - 1, start[1] - 1)
    TR = (start[0] - 1, start[1] + 1)
    BL = (start[0] + 1, start[1] - 1)
    BR = (start[0] + 1, start[1] + 1)

    def explore(start, explored) -> bool:
        if explored[start]:
            return False
        queue = [start]
        while queue:
            pos = queue.pop(0)
            y, x = pos
            if y < 0 or x < 0 or y > ymax or x > xmax:
                return False
            if explored[pos]:
                continue
            explored[pos] = True
            queue += [
                (pos[0] - 1, pos[1]),
                (pos[0] + 1, pos[1]),
                (pos[0], pos[1] - 1),
                (pos[0], pos[1] + 1),
            ]
        return True
    
    if explore(TL, explored):
        inside = TL
    elif explore(TR, explored):
        inside = TR
    elif explore(BL, explored):
        inside = BL
    elif explore(BR, explored):
        inside = BR

    explored[...] = dists >= 0
    explore(inside, explored)
    explored[dists >= 0] = False

    plt.figure()
    plt.imshow(explored)
    plt.show()

    inds = explored[1::3, 1::3]

    plt.figure()
    plt.imshow(inds)
    plt.show()

    print("No. tiles inside:", np.count_nonzero(inds))

if __name__ == "__main__":
    main()
