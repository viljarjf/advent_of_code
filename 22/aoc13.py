import json

def comp(l1, l2) -> bool:
    for i, j in zip(l1, l2):
        if isinstance(i, int) and isinstance(j, int):
            if i == j:
                continue
            return i < j
        elif isinstance(i, list) and isinstance(j, list):
            res = comp(i, j)
            if res is None and len(i) == len(j):
                continue
            return res
        elif isinstance(i, int):
            res = comp([[i]], [j])
            if res is None and len(j) == 1:
                continue
            return res
        else:
            res = comp([i], [[j]])
            if res is None and len(i) == 1:
                continue
            return res
    if len(l1) == len(l2):
        return None
    return len(l1) < len(l2)

with open("input13.txt", "r") as f:
    s = 0
    l = f.readlines()
    packages = []

    for i in range(0, len(l) - 1, 3):
        l1 = json.loads(l[i])
        packages.append(l1)
        l2 = json.loads(l[i + 1])
        packages.append(l2)

        if comp(l1, l2):
            s += i//3 + 1

print(s)

packages.append([[2]])
packages.append([[6]])

import functools
cmp = lambda l1, l2: 1 - comp(l1, l2) * 2
sorted_packages = sorted(packages, key = functools.cmp_to_key(cmp))

ind1 = sorted_packages.index([[2]]) + 1
ind2 = sorted_packages.index([[6]]) + 1
print(ind1 * ind2)
