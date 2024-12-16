import numpy as np

def get_map(test: bool = True):
    with open("10_test" if test else "10", "r") as f:
        return np.array([[int(char) for char in line.strip()] for line in f])
    
def get_indices_of_height(top_map: np.ndarray, height: int) -> list[tuple[int, int]]:
    return np.argwhere(top_map == height)

def get_trailheads(top_map: np.ndarray) -> list[tuple[int, int]]:
    return get_indices_of_height(top_map, 0)

def get_trailhead_score(top_map: np.ndarray, trailhead: tuple[int, int]) -> int:
    # BFS
    current = [trailhead]
    for i in range(1, 10):
        nexts = []
        next_height = get_indices_of_height(top_map, i)
        for pos in current:
            for possible in next_height:
                if (abs(pos[0] - possible[0]) + abs(pos[1] - possible[1])) == 1:
                    nexts.append(tuple(possible))
        current = list(set(nexts))
    return len(current)

def get_trailhead_rating(top_map: np.ndarray, trailhead: tuple[int, int]) -> int:
    # DFS
    out = 0
    queue = [(trailhead, 0)]
    while queue:
        pos, height = queue.pop()
        if height == 9:
            out += 1
            continue
        for possible in get_indices_of_height(top_map, height + 1):
            if (abs(pos[0] - possible[0]) + abs(pos[1] - possible[1])) == 1:
                queue.append((tuple(possible), height + 1))
    return out

def main():
    top_map = get_map(False)
    trailheads = get_trailheads(top_map)
    print(sum(get_trailhead_score(top_map, trailhead) for trailhead in trailheads))
    print(sum(get_trailhead_rating(top_map, trailhead) for trailhead in trailheads))


if __name__ == "__main__":
    main()
