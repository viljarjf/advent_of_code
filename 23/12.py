from typing import Iterable
import numpy as np
from fractions import Fraction

# Idea: make all permutations of the size of the spaces between the numbers.
# Check which are possible with the given limitation imposed by the board

def get_spaces(line: list[int], ans: str) -> Iterable[list[int]]:

    # add a space to each element
    line = [i + 1 for i in line]
    line[-1] -= 1

    space_size = len(ans) - sum(line)

    num_spaces = len(line) + 1

    def divide(items: int, boxes: int, layer: int, ans: str) -> str:
        if boxes == 2:
            for i in range(items + 1):
                yield [i + 1, line[-1], items - i]
        else:
            for i in range(items + 1):
                cur_ans = [i + bool(layer), line[layer] - 1]
                cur_str = "." * cur_ans[0] + "#" * cur_ans[1]
                if not compare_line_str(ans[:len(cur_str)], cur_str):
                    continue
                for d in divide(items - i, boxes - 1, layer + 1, ans[len(cur_str):]):
                    yield cur_ans + d

    for spaces in divide(space_size, num_spaces, 0, ans):
        yield spaces

def get_reprs(line: list[int], ans: str) -> Iterable[str]:

    for spaces in get_spaces(line, ans):
        out = get_repr(spaces)
        if compare_line_str(ans, out):
            yield out

def get_repr(spacing):
    cs = ".#" * len(spacing)
    out = ""
    for i, el in enumerate(spacing):
        out += cs[i] * el
    return out

def compare_line_str(line: str, repr: str) -> bool:
    for a, b in zip(line, repr):
        if a == "?":
            continue
        if a != b:
            return False
    return True

def main():
    
    num_possible = 0
    long_num_possible = 0
    from tqdm import tqdm
    with open("12", "r", encoding="utf-8") as inp, tqdm(total=1000) as pbar:
        for line in inp:
            line, blocks = line.strip().split(" ")
            blocks = [int(i) for i in blocks.split(",")]

            num_possible += sum(1 for _ in get_reprs(blocks, line))

            repetitions = 5
            line = "?".join([line] * repetitions)
            blocks = blocks * repetitions

            long_num_possible += sum(1 for _ in get_reprs(blocks, line))
            
            pbar.update(1)

    print()
    print(num_possible)
    print(long_num_possible)
    
if __name__ == "__main__":
    import time
    start = time.perf_counter()
    main()
    print(time.perf_counter() - start)