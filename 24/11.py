# Disgusting and unreadable, but fairly performant in the end

from functools import cache
from collections import defaultdict

test = [125, 17]
real = [2, 72, 8949, 0, 981038, 86311, 246, 7636740]

def get_counts(stones: list[int]) -> dict[int, int]:
    return {stone: stones.count(stone) for stone in set(stones)}

def merge_counts(*dicts: dict[int, int]) -> dict[int, int]:
    out = defaultdict(lambda: 0)
    for d in dicts:
        for key, val in d.items():
            out[key] += val
    return dict(out)

def sum_counts(*dicts: dict[int, int]):
    d = merge_counts(*dicts)
    return sum(d.values())

@cache
def handle_single(stone: int, blinks: int) -> list[int]:
    if blinks == 0:
        return [stone]
    
    if stone == 0:
        return handle_single(1, blinks - 1)
    # Rule 2
    if len(str(stone)) % 2:
        return handle_single(stone * 2024, blinks - 1)
    # Rule 1
    else:
        s = str(stone)
        l = len(s)
        return (
            handle_single(int(s[:l // 2]), blinks - 1) +
            handle_single(int(s[l // 2:]), blinks - 1)
        )

def handle_count_dict(stones_count: dict[int, int], blinks: int) -> dict[int, dict[int, int]]:
    stones = list(stones_count.keys())
    counts = []
    for stone in stones:
        res = handle_single(stone, blinks)
        counts.append(get_counts(res))

    return {stone: count for stone, count in zip(stones, counts)}

def merge_handle_count_dict_output(stones: dict[int, int], output: dict[int, dict[int, int]]) -> dict[int, int]:
    return merge_counts(*(
        {inner_key : inner_val * stones[key] for inner_key, inner_val in d.items()} for key, d in output.items()
    ))

def iterative(delta: int, total: int, testing: bool = False):
    assert total % delta == 0, "total / delta must be integer"
    stones = {stone: 1 for stone in (test if testing else real)}
    for _ in range(0, total, delta):
        new = handle_count_dict(stones, delta)
        print(sum(stones[key] * sum_counts(new[key]) for key in new))
        stones = merge_handle_count_dict_output(stones, new)
    return stones


def main():
    iterative(5, 25)
    iterative(5, 75)

if __name__ == "__main__":
    main()
