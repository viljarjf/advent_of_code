from itertools import product
from typing import Callable

def reduce(vals: list[int], ops: list[Callable[[int, int], int]]) -> int:
    out = vals[0]
    for i, op in zip(vals[1:], ops):
        out = op(out, i)
    return out

def is_constructable(ans: int, nums: list[int], ops: list[Callable[[int, int], int]]) -> bool:
    for ops_comb in product(ops, repeat = len(nums) - 1):
        if reduce(nums, ops_comb) == ans:
            return True
    return False

def plus(a: int, b: int) -> int: return a + b
def mul(a: int, b: int) -> int: return a * b
def concat(a: int, b: int) -> int: return int(str(a) + str(b))

def main():
    with open("07", "r") as f:
        task_1 = 0
        task_2 = 0
        for line in f:
            ans, nums = line.strip().split(": ")
            ans = int(ans)
            nums = [int(i) for i in nums.split()]
            if is_constructable(ans, nums, [plus, mul]):
                task_1 += ans
                task_2 += ans
            elif is_constructable(ans, nums, [plus, mul, concat]):
                task_2 += ans
    print(task_1)
    print(task_2)

if __name__ == "__main__":
    main()
