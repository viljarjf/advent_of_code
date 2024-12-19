import heapq

import numpy as np

def get_maze(testing: bool = False) -> np.ndarray:
    with open("16_test" if testing else "16", "r") as f:
        return np.array([[c == "#" for c in line.strip()] for line in f]).astype(int)

def get_min_paths(maze: np.ndarray) -> tuple[int, list[list[tuple[int, int]]]]:
    start = (maze.shape[0] - 2, 1)
    end = (1, maze.shape[1] - 2)

    q = [(0, start, (0, 1), [])]
    lowest_score_paths = []
    min_score = float("inf")
    min_scores = np.zeros_like(maze) + 1_000_000
    while q:
        val, pos, dir, path = heapq.heappop(q)
        if val > min_score:
            break
        if pos == end:
            lowest_score_paths.append(path + [pos])
            min_score = val
        if min_scores[pos] + 1000 < val:
            continue
        min_scores[pos] = val + 1000
        new = (
            pos[0] + dir[0],
            pos[1] + dir[1],
        )
        if not maze[new]:
            min_scores[pos] -= 1000
            heapq.heappush(q, (val + 1, new, dir, path + [pos]))
        dir = (-dir[1], dir[0])
        new = (
            pos[0] + dir[0],
            pos[1] + dir[1],
        )
        if not maze[new]:
            heapq.heappush(q, (val + 1001, new, dir, path + [pos]))
        dir = (-dir[0], -dir[1])
        new = (
            pos[0] + dir[0],
            pos[1] + dir[1],
        )
        if not maze[new]:
            heapq.heappush(q, (val + 1001, new, dir, path + [pos]))

    if min_score == float("inf"):
        raise ValueError("Could not solve maze")
    
    return min_score, lowest_score_paths

def main():
    maze = get_maze()
    score, paths = get_min_paths(maze)
    print(score)
    print(len(set(sum(paths, []))))

if __name__ == "__main__":
    main()
