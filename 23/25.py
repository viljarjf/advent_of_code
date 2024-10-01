import numpy as np
from matplotlib import pyplot as plt

def get_data(filename: str) -> tuple[list[str], np.ndarray]:
    """Column lookup and connectivity matrix"""
    names = []
    with open(filename, "r") as f:
        for line in f:
            for name in line.strip().split():
                names.append(name[:3])
    names = list(set(names))
    out = np.zeros((len(names), len(names)), dtype=int)
    with open(filename, "r") as f:
        for line in f:
            key, vals = line.strip().split(":")
            key_ind = names.index(key)
            for val in vals.split():
                val_ind = names.index(val)
                out[key_ind, val_ind] = 1
                out[val_ind, key_ind] = 1
    return names, out

def matpow(x: np.ndarray, n: int) -> np.ndarray:
    v, M = np.linalg.eigh(x.astype(int))
    return M @ np.diagflat(v ** n) @ M.T

def split(names: list[str], connections: np.ndarray) -> tuple[list[str], list[str]]:
    conns = connections.copy().astype(int)
    
    # increase density
    val = np.log(matpow(conns, 10) + 0.1)
    t = np.median(val)
    conns = (val < t).astype(int)

    # 2 iterations worked well
    val = np.log(matpow(conns, 5) + 0.1)
    t = np.mean(val)
    conns = (val > t).astype(int)

    out_1 = [name for name, conn in zip(names, conns[0]) if conn]
    out_2 = [name for name in names if name not in out_1]
    return out_1, out_2

def find_mistakes(names: list[str], connections: np.ndarray, group_1: list[str], group_2: list[str]):
    mistakes = []
    for name in group_1:
        ind = names.index(name)
        for i, conn in enumerate(connections[ind]):
            if conn and names[i] in group_2:
                mistakes.append((ind, i))
    return list(set(mistakes))

def main():
    names, conn = get_data("25")

    a, b = split(names, conn)

    mist = find_mistakes(names, conn, a, b)
    assert len(mist) == 3

    print(len(a) * len(b))

if __name__ == "__main__":
    main()
