import numpy as np
from itertools import combinations

def main():

    with open("11", "r", encoding="utf-8") as inp:
        original_coords: list[tuple[int, int]] = []
        for i, line in enumerate(inp):
            for j, char in enumerate(line):
                if char == "#":
                    original_coords.append((i, j))
    shape = (i, j)
    coords: np.ndarray = np.array(original_coords)

    extra_row_inds = []
    for i in range(shape[0]):
        if not np.any(coords[:, 0] == i):
            extra_row_inds.append(i)
    
    extra_col_inds = []
    for j in range(shape[1]):
        if not np.any(coords[:, 1] == j):
            extra_col_inds.append(j)

    for row in reversed(extra_row_inds):
        coords[:, 0][coords[:, 0] > row] += 1

    for col in reversed(extra_col_inds):
        coords[:, 1][coords[:, 1] > col] += 1

    d = []
    for i, j in combinations(coords, 2):
        d.append(np.sum(np.abs(i - j)))

    print(sum(d))

    coords = np.array(original_coords)

    for row in reversed(extra_row_inds):
        coords[:, 0][coords[:, 0] > row] += 1000000 - 1

    for col in reversed(extra_col_inds):
        coords[:, 1][coords[:, 1] > col] += 1000000 - 1

    d = []
    for i, j in combinations(coords, 2):
        d.append(int(np.sum(np.abs(i - j))))

    print(sum(d))

if __name__ == "__main__":
    main()
