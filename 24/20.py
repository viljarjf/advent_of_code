import numpy as np

TRACK = 0
WALL = 1
START = 2
END = 3

def get_track(testing: bool = False) -> np.ndarray:
    lookup = {
        ".": TRACK,
        "#": WALL,
        "S": START,
        "E": END
    }
    with open("20_test" if testing else "20", "r") as f:
        return np.array([[lookup[c] for c in line.strip()] for line in f])

def get_track_path(track: np.ndarray) -> list[tuple[int, int]]:
    start = tuple(np.argwhere(track == START)[0])
    end = tuple(np.argwhere(track == END)[0])
    out = [start]
    pos = start
    while pos != end:
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new = (pos[0] + dir[0], pos[1] + dir[1])
            if new not in out and track[new] != WALL:
                out.append(new)
                pos = new
                break
    return out

def get_path_distances(path: list[tuple[int, int]]) -> np.ndarray:
    out = np.zeros((len(path), len(path)), dtype=int)
    for i, pi in enumerate(path):
        for j, pj in enumerate(path):
            if j > i: break
            out[i, j] = abs(pi[0] - pj[0]) + abs(pi[1] - pj[1])
    return out

def main():
    track = get_track()
    path = get_track_path(track)
    dist = get_path_distances(path)

    res = np.unique_counts(np.abs(np.diff(np.argwhere(dist == 2))) - 2)

    print(np.sum(res.counts[res.values >= 100]))

    big = [np.abs(np.diff(np.argwhere(dist == d))) - d for d in range(2, 21)]
    res = np.unique_counts(np.concatenate(big))
    print(np.sum(res.counts[res.values >= 100]))


if __name__ == "__main__":
    main()
