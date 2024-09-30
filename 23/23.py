import numpy as np
from matplotlib import pyplot as plt

WALL = 0
PATH = 1
ICE_UP = 2
ICE_RIGHT = 3
ICE_DOWN = 4
ICE_LEFT = 5

LOOKUP = {
    "#": WALL,
    ".": PATH,
    "^": ICE_UP,
    ">": ICE_RIGHT,
    "v": ICE_DOWN,
    "<": ICE_LEFT
}

def find_intersections(map: np.ndarray) -> list[tuple[int, int]]:
    out = [
        (0, 1), # start
    ]

    for ind in np.ndindex(map.shape):
        # Skip edges
        if ind[0] == 0 or ind[1] == 0 or ind[0] == map.shape[0] - 1 or ind[1] == map.shape[1] - 1:
            continue
        if map[ind]:
            # count neighbouring sites
            if sum(map[tile] != WALL for tile in [
                (ind[0] - 1, ind[1]),
                (ind[0] + 1, ind[1]),
                (ind[0], ind[1] - 1),
                (ind[0], ind[1] + 1),
            ]) > 2:
                out.append(ind)
    out.append((map.shape[0] - 1, map.shape[1] - 2)) # end
    return out

def explore_single(map: np.ndarray, pos: tuple[int, int], initial: tuple[int, int], intersections: list[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int], int]:
    dy, dx = pos[0] - initial[0], pos[1] - initial[1]
    if [
        True,       # Wall
        False,      # Path
        dy != -1,   # up
        dx != 1,    # right
        dy != 1,    # down
        dx != -1,   # left
    ][map[pos]]:
        return None
    queue = [pos]
    explored = [initial]
    segment_length = 1
    while queue:
        pos = queue.pop(0)
        if pos in explored:
            continue
        explored.append(pos)
        if pos in intersections:
            break
        if map[pos] == WALL:
            continue
        segment_length += 1
        queue.append((pos[0] + 1, pos[1]))
        queue.append((pos[0] - 1, pos[1]))
        queue.append((pos[0], pos[1] + 1))
        queue.append((pos[0], pos[1] - 1))

    return (
        initial, # start
        pos,     # end
        segment_length
    )

def explore(map: np.ndarray):
    intersections = find_intersections(map)
    out = []

    # Explore from start to first intersection
    out.append(explore_single(map, (1, 1), (0, 1), intersections))
    # Explore the rest (except the end)
    for intersection in intersections[1:-1]:
        for pos in [
            (intersection[0] + 1, intersection[1]),
            (intersection[0] - 1, intersection[1]),
            (intersection[0], intersection[1] + 1),
            (intersection[0], intersection[1] - 1),
        ]:
            if (res := explore_single(map, pos, intersection, intersections)) is not None:
                out.append(res)
    return out

def find_maximum_length(graph: list[tuple[tuple[int, int], tuple[int, int], int]]) -> int:
    max_y = max(i[1][0] for i in graph)
    target = (max_y, max_y - 1)
    queue = [(
        (0, 1), # start
        0       # length
    )]
    while queue:
        pos, length = queue.pop(0)
        if pos == target:
            break
        
    return length

def plot(map):
    plt.figure()
    plt.imshow(map)
    plt.show()

def main():
    
    map = []
    with open("23_test", "r") as f:
        for line in f:
            map.append([LOOKUP[tile] for tile in line.strip()])
    map = np.array(map)

    graph = explore(map)
    plot(map)

    print("\n".join(str(i) for i in graph))


if __name__ == "__main__":
    main()
