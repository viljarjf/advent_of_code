import numpy as np

sensors = []
beacons = []
with open("input15.txt", "r") as f:
    for l in f:
        l = l.split()
        sx = int(l[2][2:-1])
        sy = int(l[3][2:-1])
        bx = int(l[8][2:-1])
        by = int(l[9][2:])
        sensors.append((sx, sy))
        beacons.append((bx, by))

sensors = np.array(sensors)
beacons = np.array(beacons)


def find_empty(
    row: int, 
    start: int = None, 
    end: int = None, 
    include_sensors: bool = False, 
    return_hole: bool = False
    ) -> int:
    ranges = []

    for i in range(len(sensors)):
        sx, sy = sensors[i, :]
        bx, by = beacons[i, :]

        dx = abs(bx - sx)
        dy = abs(by - sy)
        d = dx + dy

        d_to_row = abs(sy - row)

        x = d - d_to_row
        if x > 0:
            ranges.append((sx - x, sx + x))
    
    ranges.sort(key = lambda i: i[0])
    R_min, R_max = ranges[0]
    if start is None:
        start = R_min
    if end is None:
        end = float("inf")
        
    x_empty = 0
    for r_min, r_max in ranges:
        if R_max > end:
            R_max = end
            break
        if r_min <= R_max:
            R_max = max(r_max, R_max)
        else:
            if return_hole:
                return int(r_min) - 1
            x_empty += R_max - max(R_min, start)
            R_min = r_min
            R_max = r_max
    x_empty += min(R_max, end) - max(R_min, start)

    if include_sensors:
        x_empty -= np.count_nonzero(
            (sensors[:, 1] == row) & 
            (sensors[:, 0] >= start) & 
            (sensors[:, 0] <= end)
            )
    
    return x_empty

row = 2000000
x_empty = find_empty(row)
print(x_empty)

search_max = 4000000
for y in range(search_max):
    search = find_empty(y, 0, search_max, False, True)
    if not y % 1000:
        print(f"@ {y = }")
    if search < search_max:
        x = search
        print(f"{x = }, {y = }")
        print(x*search_max + y)
        break
