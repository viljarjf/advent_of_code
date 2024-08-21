import numpy as np
import matplotlib
matplotlib.use("QtAgg")
from matplotlib import pyplot as plt

PATH = 1
BUSH = 0
START = 10

def get_board(filename: str, pad: int = 0) -> tuple[np.ndarray, np.ndarray]:
    map = []
    with open(filename, "r") as f:
        for line in f:
            map.append([PATH if c == "." else BUSH if c == "#" else START for c in line.strip()])
    map = np.array(map)
    pos = map == START
    map[pos] = PATH
    map = map.astype(bool)
    
    map = np.tile(map, (2 * pad + 1, 2 * pad + 1))
    pos = np.pad(pos, pad * np.array(pos.shape), constant_values=0)

    return map, pos

def move(map: np.ndarray, pos: np.ndarray) -> np.ndarray:
    return (
        np.roll(pos, 1, 0) |
        np.roll(pos, -1, 0) |
        np.roll(pos, 1, 1) |
        np.roll(pos, -1, 1)
    ) & map

def mask_voids(map: np.ndarray) -> np.ndarray:
    pos = np.zeros_like(map)
    pos[0, 0] = 1
    visited = np.copy(pos)
    for _ in range(sum(map.shape)):
        pos = move(map, pos)
        visited |= pos
    return map & pos

def checkerboard(shape: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    out = np.empty(shape, dtype=bool)
    val = True
    for pos in np.ndindex(shape):
        out[pos] = val
        val ^= True
    return ~out, out

def diamond(shape: tuple[int, int]) -> np.ndarray:
    out = np.empty(shape, dtype=bool)
    for pos in np.ndindex(shape):
        out[pos] = np.sum(np.abs(np.array(pos) - np.array(shape) // 2)) <= (shape[0] / 2)
    return out

def main():
    map, pos = get_board("21", 0)

    for _ in range(64):
        pos = move(map, pos)
    print(np.count_nonzero(pos))

    ch1, ch2 = checkerboard(map.shape)
    dm = diamond(map.shape)

    a = map & ch1 & dm
    b = map & ch2 & dm
    c = map & ch1 & ~dm
    d = map & ch2 & ~dm
    an = np.count_nonzero(a)
    bn = np.count_nonzero(b)
    cn = np.count_nonzero(c)
    dn = np.count_nonzero(d)

    target = 26501365 - 65
    n, remainder = divmod(target, 131)

    def total(n: int) -> int:
        return an * (n + 1) ** 2 + bn * n ** 2 + (n * (n + 1)) * (cn + dn - 1)
    
    print(total(n))
    print(f"{remainder = }")

if __name__ == "__main__":
    main()
