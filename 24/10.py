import numpy as np

def get_map(test: bool = True):
    with open("10_test" if test else "10", "r") as f:
        return np.array([[int(char) for char in line.strip()] for line in f])

def get_trailheads(top_map: np.ndarray) -> list[tuple[int, int]]:
    ...

def get_trailhead_score(trailhead: tuple[int, int]) -> int:
    ...

def main():
    top_map = get_map()
    trailheads = get_trailheads(top_map)
    print(sum(get_trailhead_score(trailhead) for trailhead in trailheads))


if __name__ == "__main__":
    main()
