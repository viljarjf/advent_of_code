import heapq

import numpy as np

def get_ram() -> list[tuple[int, int]]:
    out = []
    with open("18", "r") as f:
        for line in f:
            a, b = line.strip().split(",")
            out.append((int(a), int(b)))
    return out

def get_maze(ram: list[tuple[int, int]]) -> np.ndarray:
    out = np.zeros((71, 71), dtype=int)
    for pos in ram:
        out[pos] = 1
    return out

def get_shortest_path_length(maze: np.ndarray) -> int:
    start = (0, 0)
    end = (maze.shape[0] - 1, maze.shape[1] - 1)
    q = [(0, start, [])]
    visited = np.zeros(maze.shape, dtype=bool)
    while q:
        dist, pos, path = heapq.heappop(q)
        visited[pos] = True
        if pos == end:
            return dist
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new = (pos[0] + dir[0], pos[1] + dir[1])
            if (
                0 <= new[0] < maze.shape[0] and 
                0 <= new[1] < maze.shape[1] and 
                not maze[new] and 
                not visited[new]
            ):
                visited[new] = True
                heapq.heappush(q, (dist + 1, new, path + [pos]))
    return None
def main():
    ram = get_ram()
    maze = get_maze(ram[:1024])
    print(get_shortest_path_length(maze))
    
    lower = 1024
    upper = len(ram) - 1
    while upper - lower > 1:
        n = (upper + lower) >> 1
        m = get_maze(ram[:n])
        if get_shortest_path_length(m) is None:
            upper = n
        else:
            lower = n
    print(ram[lower])

if __name__ == "__main__":
    main()
