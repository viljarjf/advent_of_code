import numpy as np

data = []
star_ind = -2
with open("03", "r", encoding="utf-8") as inp:
    for line in inp:
        data_line = []
        num = ""
        num_found = False
        for char in line.strip():
            if char.isnumeric():
                num_found = True
                num += char
            else:
                if num_found:
                    num_found = False
                    data_line += [int(num)] * len(num)
                    num = ""
                if char == ".":
                    data_line.append(0)
                elif char == "*":
                    data_line.append(star_ind)
                    star_ind -= 1
                else:
                    data_line.append(-1)
        if num_found:
            data_line += [int(num)] * len(num)
        data.append(data_line)
data = np.array(data)

chars = data.copy()
chars[chars > 0] = 0
chars[chars < 0] = 1

stars = data.copy()
stars[stars > 0] = 0
stars[stars == -1] = 0
stars *= -1
stars[stars > 0] -= 1

data[data < 0] = 0

from scipy.ndimage import binary_dilation

structure = np.ones((3, 3), dtype=bool)

s = 0
for num in np.unique(data):
    inds = binary_dilation(data == num, structure)
    s += num * np.sum(chars[inds])
print(s)

s = 0
for num in np.unique(stars):
    if num == 0:
        continue
    inds = binary_dilation(stars == num, structure)
    d = data[inds]
    d = np.unique(d[d > 0])
    if len(d) <= 1:
        continue
    s += np.prod(d)

print(s)