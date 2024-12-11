import numpy as np

def get_map(test: bool = True):
    with open("10_test" if test else "10", "r") as f:
        return np.array([[int(char) for char in line.strip()] for line in f])
    
def get_indices_of_height(top_map: np.ndarray, height: int) -> list[tuple[int, int]]:
    return np.argwhere(top_map == height)

def get_trailheads(top_map: np.ndarray) -> list[tuple[int, int]]:
    return get_indices_of_height(top_map, 0)

def get_trailhead_score(top_map: np.ndarray, trailhead: tuple[int, int]) -> int:
    current = [trailhead]
    for i in range(1, 10):
        next = []
        next_height = get_indices_of_height(top_map, i)
        for pos in current:
            for possible in next_height:
                if (abs(pos[0] - possible[0]) + abs(pos[1] - possible[1])) == 1:
                    next.append(possible)
        print(next)
        current = next
    return len(current)

def main():
    top_map = get_map()
    trailheads = get_trailheads(top_map)
    print(get_trailhead_score(top_map, trailheads[0]))
    # print(sum(get_trailhead_score(top_map, trailhead) for trailhead in trailheads))


if __name__ == "__main__":
    main()
