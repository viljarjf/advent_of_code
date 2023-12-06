data = []
import numpy as np

with open("input12.txt", "r") as f:
    for i, l in enumerate(f):
        if "S" in l:
            start = (i, l.index("S"))
            l = l.replace("S", "a")
        if "E" in l:
            end = (i, l.index("E"))
            l = l.replace("E", "z")
        data.append([ord(c) for c in l.strip()])
data = np.array(data)
climbing_height = 1

def shortest_road(heightmap: list[list[int]], start: tuple[int, int], end_function):
    # BFS
    # copied from my algorithms and data structures exercise

    x_max = len(heightmap) - 1
    y_max = len(heightmap[0]) - 1
    #    1
    #  2 x 3
    #    4
    path = [[0 for __ in range(y_max + 1)] for _ in range(x_max + 1)]
    q = [start]
    while q:
        node = q.pop(0)
        if end_function(node):
            break
        x, y = node
        p = path[x][y]
        height = heightmap[x][y]
        if x > 0 and p != 2:
            if heightmap[x-1][y] - height <= climbing_height and path[x-1][y] == 0:
                q.append((x-1, y))
                path[x-1][y] = 3
        if x < x_max and p != 3:
            if heightmap[x+1][y] - height <= climbing_height and path[x+1][y] == 0:
                q.append((x+1, y))
                path[x+1][y] = 2
        if y > 0 and p != 1:
            if heightmap[x][y-1] - height <= climbing_height and path[x][y-1] == 0:
                q.append((x, y-1))
                path[x][y-1] = 4
        if y < y_max and p != 4:
            if heightmap[x][y+1] - height <= climbing_height and path[x][y+1] == 0:
                q.append((x, y+1))
                path[x][y+1] = 1
    else:
        return None

    # reconstruct path
    res = [node]
    while node != start:
        x, y = node
        p = path[x][y]
        if p == 1:
            node = (x, y-1)
        elif p == 2:
            node = (x-1, y)
        elif p == 3:
            node = (x+1, y)
        else:
            node = (x, y+1)
        res.append(node)
    res.reverse()
    return res

def find_end(node):
    return node == end

path = shortest_road(data, start, find_end)
print(len(path) - 1)

data = np.max(data) - data
def find_low(node):
    x, y = node
    return data[x][y] == ord("z") - ord("a")

shortpath = shortest_road(data, end, find_low)
print(len(shortpath) - 1)
