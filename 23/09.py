def main():
    seqs = []
    with open("09", "r", encoding="utf-8") as inp:
        for line in inp:
            seq = line.strip().split(" ")
            seqs.append([int(i) for i in seq])

    def forward_extrapolate(seq: list[int]) -> int:
        if all(s == 0 for s in seq):
            return 0
        next_seq = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
        return seq[-1] + forward_extrapolate(next_seq)

    def backward_extrapolate(seq: list[int]) -> int:
        if all(s == 0 for s in seq):
            return 0
        next_seq = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
        return seq[0] - backward_extrapolate(next_seq)

    nexts = [forward_extrapolate(s) for s in seqs]
    print(sum(nexts))

    prevs = [backward_extrapolate(s) for s in seqs]
    print(sum(prevs))


if __name__ == "__main__":
    main()
