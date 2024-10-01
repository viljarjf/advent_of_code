import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict


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

Node = tuple[tuple[int, int], tuple[int, int], list[tuple[int, int]]]
FullGraph = list[Node]
Graph = list[tuple[tuple[int, int], tuple[int, int], int]]

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

def explore_single(map: np.ndarray, pos: tuple[int, int], initial: tuple[int, int], intersections: list[tuple[int, int]]) -> Node:
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
    queue = [(pos, [])]
    explored = [initial]
    while queue:
        pos, segment = queue.pop(0)
        if pos in explored:
            continue
        explored.append(pos)
        if pos in intersections:
            break
        if map[pos] == WALL:
            continue
        queue.append(((pos[0] + 1, pos[1]), segment + [pos]))
        queue.append(((pos[0] - 1, pos[1]), segment + [pos]))
        queue.append(((pos[0], pos[1] + 1), segment + [pos]))
        queue.append(((pos[0], pos[1] - 1), segment + [pos]))

    return (
        initial, # start
        pos,     # end
        segment + [pos]
    )

def explore(map: np.ndarray) -> FullGraph:
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

def find_maximum_length_path(graph: Graph) -> list[tuple[int, int]]:
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    edge_lengths = {}
    for edge in graph:
        start, end, length = edge
        outgoing[start].append(end)
        incoming[end].append(start)
        edge_lengths[start + end] = length
    
    start = (0, 1)
    max_y = max(i[1][0] for i in graph)
    end = (max_y, max_y - 1)

    incoming[start] = []
    outgoing[end] = []
    
    lengths = defaultdict(lambda: 0)
    queue = [(
        0,
        start,
        [start]
    )]
    end_path = []
    i = 0
    while queue:
        i += 1
        length, pos, visited = queue.pop()
        if length > lengths[pos]:
            lengths[pos] = length
            if pos == end:
                end_path = visited
        for edge in outgoing[pos]:
            if edge in visited:
                continue
            queue.append((
                length + edge_lengths[pos + edge],
                edge,
                visited + [edge]
            ))
    return end_path

def plot(map: np.ndarray):
    plt.figure()
    plt.imshow(map)
    plt.axis("off")
    plt.show()

def plot_path(map: np.ndarray, path: list[tuple[int, int]], graph_with_segments: FullGraph):
    map = map.copy()
    map[map > 0] = 1
    segments = {start + end : segment for start, end, segment in graph_with_segments}
    for start, end in zip(path[:-1], path[1:]):
        for tile in segments[start + end]:
            map[tile] = 2
    for pos in path:
        map[pos] = 3
    plot(map)

def full_workflow(graph_with_segments: FullGraph, map: np.ndarray):
    graph = [(start, end, len(segment)) for start, end, segment in graph_with_segments]
    lengths = {start + end : length for start, end, length in graph}
    longest_path = find_maximum_length_path(graph)
    plot_path(map, longest_path, graph_with_segments)
    lengths = {start + end : length for start, end, length in graph}
    print(sum(lengths[start + end] for start, end in zip(longest_path[:-1], longest_path[1:])))

def main():
    
    map = []
    with open("23", "r") as f:
        for line in f:
            map.append([LOOKUP[tile] for tile in line.strip()])
    map = np.array(map)

    graph = explore(map)
    full_workflow(graph, map)
    
    for start, end, length in graph.copy():
        graph.append((end, start, length))
    full_workflow(graph, map)

if __name__ == "__main__":
    main()
