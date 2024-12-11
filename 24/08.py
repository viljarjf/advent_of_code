from collections import defaultdict
from itertools import combinations

def get_area(test: bool = True) -> tuple[dict[str, list[tuple[int, int]]], tuple[int, int]]:
    out = defaultdict(list)
    with open("08_test" if test else "08", "r") as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line.strip()):
                if char != ".":
                    out[char].append((i, j))
    return out, (i, j)


def get_simple_antinodes(stations: dict[str, list[tuple[int, int]]], size: tuple[int, int]) -> list[tuple[int, int]]:
    out = []
    for positions in stations.values():
        for pos_1, pos_2 in combinations(positions, 2):
            delta = (
                pos_2[0] - pos_1[0], 
                pos_2[1] - pos_1[1],
            )
            out += [
                (pos_1[0] - delta[0], pos_1[1] - delta[1]),
                (pos_2[0] + delta[0], pos_2[1] + delta[1]),
            ]
    out = filter(lambda pos: 0 <= pos[0] <= size[0] and 0 <= pos[1] <= size[1], out)
    return list(set(out))

def get_all_antinodes(stations: dict[str, list[tuple[int, int]]], size: tuple[int, int]) -> list[tuple[int, int]]:
    out = []
    for positions in stations.values():
        for pos_1, pos_2 in combinations(positions, 2):
            delta = (
                pos_2[0] - pos_1[0], 
                pos_2[1] - pos_1[1],
            )
            for i in range(max(size[0] // delta[0], size[1] // delta[1])):
                out += [
                    (pos_1[0] - i * delta[0], pos_1[1] - i * delta[1]),
                    (pos_2[0] + i * delta[0], pos_2[1] + i * delta[1]),
                ]
    out = filter(lambda pos: 0 <= pos[0] <= size[0] and 0 <= pos[1] <= size[1], out)
    return list(set(out))

def main():
    stations, size = get_area(False)
    simple_antinodes = get_simple_antinodes(stations, size)
    print(len(simple_antinodes))
    all_antinodes = get_all_antinodes(stations, size)
    print(len(all_antinodes))

if __name__ == "__main__":
    main()
