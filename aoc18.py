import numpy as np

arr = []
max_x = max_y = max_z = 0
data = {}
with open("input18.txt", "r") as f:
    for l in f:
        k = tuple([int(i) for i in l.split(",")])
        data[k] = 1
        x, y, z = k
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)
        arr.append(k)
arr = np.array(arr)

area = 0
surface = {}

for x, y, z in data.keys():
    if data.get((x+1, y, z)) is None:
        area += 1
        if surface.get((x+1, y, z)) is None:
            surface[(x+1, y, z)] = 0
        surface[(x+1, y, z)] += 1
    if data.get((x-1, y, z)) is None:
        area += 1
        if surface.get((x-1, y, z)) is None:
            surface[(x-1, y, z)] = 0
        surface[(x-1, y, z)] += 1
    if data.get((x, y+1, z)) is None:
        area += 1
        if surface.get((x, y+1, z)) is None:
            surface[(x, y+1, z)] = 0
        surface[(x, y+1, z)] += 1
    if data.get((x, y-1, z)) is None:
        area += 1
        if surface.get((x, y-1, z)) is None:
            surface[(x, y-1, z)] = 0
        surface[(x, y-1, z)] += 1
    if data.get((x, y, z+1)) is None:
        area += 1
        if surface.get((x, y, z+1)) is None:
            surface[(x, y, z+1)] = 0
        surface[(x, y, z+1)] += 1
    if data.get((x, y, z-1)) is None:
        area += 1
        if surface.get((x, y, z-1)) is None:
            surface[(x, y, z-1)] = 0
        surface[(x, y, z-1)] += 1

print(area)

# make 3d bitmap
# fill from outside
# for each surface:
#   if not filled:
#       remove own surface area contribution from sum
AIR = 0
LAVA = 1
WATER = 2
bitmap = np.zeros((max_x + 2, max_y + 2, max_z + 2), dtype=np.byte) + AIR
for x, y, z in arr:
    bitmap[x, y, z] = LAVA

q = [(0,0,0)]
while q:
    x, y, z = q.pop()
    if x < 0 or y < 0 or z < 0 or x >= max_x + 2 or y >= max_y + 2 or z >= max_z + 2:
        continue
    if bitmap[x, y, z] == AIR:
        bitmap[x, y, z] = WATER
        q.append((x+1, y, z))
        q.append((x-1, y, z))
        q.append((x, y+1, z))
        q.append((x, y-1, z))
        q.append((x, y, z+1))
        q.append((x, y, z-1))

for x, y, z in surface.keys():
    if bitmap[x, y, z] == AIR:
        area -= surface[(x, y, z)]

print(area)