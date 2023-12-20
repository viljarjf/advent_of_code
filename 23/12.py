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
    with open("12", "r", encoding="utf-8") as inp:
        # parse
        for line in inp:
            line, blocks = line.strip().split(" ")
            blocks = [int(i) for i in blocks.split(",")]

            for repr in get_reprs(blocks, line):
                num_possible += 1
            
            s = np.array([i for i in get_spaces(blocks, line) if compare_line_str(line, get_repr(i))])
            
            line2 = "?".join([line]*2)
            blocks2 = blocks * 2
            s2 = np.array([i for i in get_spaces(blocks2, line2) if compare_line_str(line2, get_repr(i))])

            single = s.shape[0]
            increase = s2.shape[0]
            r = Fraction(increase, single)

            if r.denominator == 1:
                long_num_possible += r ** 3 * increase
                continue
            print("Long")
            print(line, blocks)

            line3 = "?".join([line]*3)
            blocks3 = blocks * 3
            s3 = np.array([i for i in get_spaces(blocks3, line3) if compare_line_str(line3, get_repr(i))])
            line4 = "?".join([line]*4)
            blocks4 = blocks * 4
            s4 = np.array([i for i in get_spaces(blocks4, line4) if compare_line_str(line4, get_repr(i))])

            print(s.shape)
            print(s2.shape)
            print(s3.shape)
            print(s4.shape)

            line5 = "?".join([line]*5)
            blocks5 = blocks * 5
            num_possible += sum(1 for _ in get_reprs(blocks5, line5))
                
    print()
    print(num_possible)
    print(long_num_possible)
    
if __name__ == "__main__":
    main()
