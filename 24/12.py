import numpy as np

def get_garden(testing: bool = False) -> np.ndarray:
    with open("12_test" if testing else "12", "r") as f:
        out = np.array([
            [ord(c) for c in line.strip()]
            for line in f
        ], dtype=int)
    out -= out.min()
    return out

def get_regions(garden: np.ndarray):
    assignments = np.zeros_like(garden)
    assignment_ind = 0
    while np.any(assignments == 0):
        queue = [np.unravel_index(np.argmin(assignments, axis=None), assignments.shape)]
        assignment_ind += 1
        plant = garden[queue[0]]
        while queue:
            pos = queue.pop()
            if not 0 <= pos[0] < garden.shape[0] or not 0 <= pos[1] < garden.shape[1]:
                continue
            if garden[pos] != plant:
                continue
            if assignments[pos] == assignment_ind:
                continue
            assignments[pos] = assignment_ind
            x, y = pos
            queue += [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]
    return [np.argwhere(assignments == i) for i in np.unique(assignments)]

def get_area(region: np.ndarray) -> int:
    assert region.shape[1] == 2
    return region.shape[0]

def get_perimeter(region: np.ndarray) -> int:
    assert region.shape[1] == 2
    perimeter = 0
    region = [tuple(i) for i in region]
    for i, j in region:
        perimeter += 4
        if (i + 1, j) in region:
            perimeter -= 1
        if (i - 1, j) in region:
            perimeter -= 1
        if (i, j + 1) in region:
            perimeter -= 1
        if (i, j - 1) in region:
            perimeter -= 1
    return perimeter

def get_num_sides(region: np.ndarray) -> int:
    assert region.shape[1] == 2
    sides = 0
    region = [tuple(i) for i in region]
    for i, j in region:
        # Convex corners
        if (i + 1, j) not in region and (i, j + 1) not in region:
            sides += 1
        if (i, j + 1) not in region and (i - 1, j) not in region:
            sides += 1
        if (i - 1, j) not in region and (i, j - 1) not in region:
            sides += 1
        if (i, j - 1) not in region and (i + 1, j) not in region:
            sides += 1
        # Concave corners
        if (i + 1, j) in region and (i, j + 1) in region and (i + 1, j + 1) not in region:
            sides += 1
        if (i, j + 1) in region and (i - 1, j) in region and (i - 1, j + 1) not in region:
            sides += 1
        if (i - 1, j) in region and (i, j - 1) in region and (i - 1, j - 1) not in region:
            sides += 1
        if (i, j - 1) in region and (i + 1, j) in region and (i + 1, j - 1) not in region:
            sides += 1
    return sides

def main():
    garden = get_garden()
    regions = get_regions(garden)
    areas = [get_area(region) for region in regions]
    perimeters = [get_perimeter(region) for region in regions]
    sides = [get_num_sides(region) for region in regions]

    print(sum(a * p for a, p in zip(areas, perimeters)))
    print(sum(a * s for a, s in zip(areas, sides)))

if __name__ == "__main__":
    main()
