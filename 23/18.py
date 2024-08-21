import numpy as np
import matplotlib

matplotlib.use("QtAgg")

from matplotlib import pyplot as plt

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRS = {"R": RIGHT, "U": UP, "L": LEFT, "D": DOWN}


def calc_area(points: list[tuple[int, int]]) -> int:
    area = 0
    for i in range(len(points)):
        a, b = points[i - 1]
        c, d = points[i]
        area -= a * d - b * c
    return area // 2


def calc_perimeter(points: list[tuple[int, int]]) -> int:
    perimeter = 0
    for i in range(len(points)):
        a, b = points[i - 1]
        c, d = points[i]
        perimeter += abs(a - c) + abs(b - d)
    return perimeter


def interior(points: list[tuple[int, int]]) -> int:
    return calc_area(points) + calc_perimeter(points) // 2 + 1


def main():
    edges = [(0, 0)]
    hex_edges = [(0, 0)]

    with open("18", "r") as f:
        for line in f:
            dir, num, color = line.split(" ")
            pos = edges[-1]
            edges.append(
                (
                    pos[0] + DIRS[dir][0] * int(num),
                    pos[1] + DIRS[dir][1] * int(num),
                )
            )

            color = color[2:-2]
            num = int("0x" + color[:-1].lower(), base=16)
            dir = "RDLU"[int(color[-1])]
            pos = hex_edges[-1]
            hex_edges.append(
                (
                    pos[0] + DIRS[dir][0] * int(num),
                    pos[1] + DIRS[dir][1] * int(num),
                )
            )

    print(interior(edges))
    print(interior(hex_edges))


if __name__ == "__main__":
    main()
