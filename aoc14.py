from matplotlib import pyplot as plt
import numpy as np

with open("input14.txt", "r") as f:
    paths = []
    for l in f:
        path = l.split("->")
        paths.append([[int(i) for i in seg.split(",")] for seg in path])


max_x = max([max([i[0] for i in paths]) for paths in paths])
max_y = max([max([i[1] for i in paths]) for paths in paths])

cave = np.zeros((max_y + 3, max_x + max_y + 3))

for path in paths:
    x0, y0 = path[0]
    for x, y in path[1:]:
        dx = 0 if not (x - x0) else 2*(x > x0) - 1
        dy = 0 if not (y - y0) else 2*(y > y0) - 1
        while True:
            cave[y0, x0] = 1
            if x0 == x and y0 == y:
                break
            x0 += dx
            y0 += dy

def main(cave):
    n = 0
    try:
        while True:
            x, y = 500, 0
            while True:
                if cave[y+1, x] == 0:
                    y += 1
                elif cave[y+1, x-1] == 0:
                    x -= 1
                    y += 1
                elif cave[y+1, x+1] == 0:
                    x += 1
                    y += 1
                elif cave[y, x] != 0:
                    raise IndexError
                else:
                    cave[y, x] = 2
                    break
            n += 1
    except IndexError:
        print(n)
        plt.imshow(cave)
        plt.show()

main(cave)

cave[cave == 2] = 0
cave[max_y + 2, :] = 1

main(cave)