import numpy as np

def find_vertical_reflection(arr: np.ndarray) -> int:
    for i in range(arr.shape[0] - 1):
        left = arr[:i + 1, :][::-1, :]
        right = arr[i + 1:, :]
        lim = min(left.shape[0], right.shape[0])
        left = left[:lim, :]
        right = right[:lim, :]
        if np.all(left == right):
            return i + 1
    return 0

def find_vertical_reflection_smudge(arr: np.ndarray) -> int:
    for i in range(arr.shape[0] - 1):
        left = arr[:i + 1, :][::-1, :]
        right = arr[i + 1:, :]
        lim = min(left.shape[0], right.shape[0])
        left = left[:lim, :]
        right = right[:lim, :]
        if np.sum(left != right) == 1:
            return i + 1
    return 0

def main():
    with open("13", "r", encoding="utf-8") as inp:
        m = []
        s1 = 0
        s2 = 0
        for line in inp:
            if line.strip():
                m.append([1 if i == "#" else 0 for i in line.strip()])
            else:
                # full mirror
                m = np.array(m)

                num_rows = find_vertical_reflection(m)
                num_cols = find_vertical_reflection(m.T)
                s1 += num_cols + 100 * num_rows

                num_rows = find_vertical_reflection_smudge(m)
                num_cols = find_vertical_reflection_smudge(m.T)
                s2 += num_cols + 100 * num_rows

                m = []
    print(s1)
    print(s2)

if __name__ == "__main__":
    main()
