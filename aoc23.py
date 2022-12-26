import numpy as np

data = []
with open("input", "r") as f:
    for i, line in enumerate(f):
        for j, char in enumerate(line):
            if char == "#":
                data.append((i, j))

def get_field(data: list[tuple[int, int]]) -> np.ndarray:
    min_x = min(i[1] for i in data)
    max_x = max(i[1] for i in data) + 1
    min_y = min(i[0] for i in data)
    max_y = max(i[0] for i in data) + 1
    out = np.zeros((max_y - min_y, max_x - min_x), dtype=np.uint8)
    for y, x in data:
        out[y - min_y, x - min_x] = 1
    return out

def print_field(data: list[tuple[int, int]]) -> str:
    field = get_field(data)
    s = ""
    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            s += "#" if field[i, j] else "."
        s += "\n"
    print(s)
    return s

order = ["N", "S", "W", "E"]


for _ in range(10000):
    targets = []
    for y, x in data:
        # check if alone
        if  (y - 1, x - 1) in data or \
            (y - 1, x - 0) in data or \
            (y - 1, x + 1) in data or \
            (y + 0, x - 1) in data or \
            (y + 0, x + 1) in data or \
            (y + 1, x - 1) in data or \
            (y + 1, x - 0) in data or \
            (y + 1, x + 1) in data:
            for dir in order:
                if dir == "N":
                    if  (y - 1, x - 1) not in data and \
                        (y - 1, x - 0) not in data and \
                        (y - 1, x + 1) not in data:
                        targets.append((y - 1, x))
                        break
                elif dir == "S":
                    if  (y + 1, x - 1) not in data and \
                        (y + 1, x - 0) not in data and \
                        (y + 1, x + 1) not in data:
                        targets.append((y + 1, x))
                        break
                elif dir == "W":
                    if  (y - 1, x - 1) not in data and \
                        (y + 0, x - 1) not in data and \
                        (y + 1, x - 1) not in data:
                        targets.append((y , x - 1))
                        break
                elif dir == "E":
                    if  (y - 1, x + 1) not in data and \
                        (y + 0, x + 1) not in data and \
                        (y + 1, x + 1) not in data:
                        targets.append((y, x + 1))
                        break
            else:
                targets.append(None)
        else:
            targets.append(None)
    n = 0
    for i, target in enumerate(targets):
        if target is None or targets.count(target) > 1:
            continue
        data[i] = target
        n += 1
    if n == 0:
        print(_)
        break
    if not _%20:
        print(_)
    order.append(order.pop(0))

print(np.count_nonzero(get_field(data) == 0))
