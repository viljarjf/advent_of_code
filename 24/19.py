from functools import cache
from typing import Callable

def get_towels_and_patterns(testing: bool = False) -> tuple[list[str], list[str]]:
    patterns = []

    with open("19_test" if testing else "19", "r") as f:
        towels = f.readline().strip().split(", ")
        f.readline()
        for line in f:
            patterns.append(line.strip())
    return towels, patterns

def find_any_solution_factory(towels: list[str]) -> Callable[[str], list[str]]:
    @cache
    def find_any_solution(pattern: str) -> list[str]:
        for towel in towels:
            if towel == pattern:
                return [towel]
            if pattern[:len(towel)] == towel:
                remaining = find_any_solution(pattern[len(towel):])
                if remaining:
                    return [towel] + remaining
        return []
    return find_any_solution

def find_num_solutions_factory(towels: list[str]) -> Callable[[str], int]:
    @cache
    def find_num_solutions(pattern: str) -> int:
        out = 0
        for towel in towels:
            if towel == pattern:
                out += 1
            elif pattern[:len(towel)] == towel:
                out += find_num_solutions(pattern[len(towel):])
        return out
    return find_num_solutions

def main():
    towels, patterns = get_towels_and_patterns(True)
    find_num_solutions = find_num_solutions_factory(towels)
    towels.sort(key=lambda el: len(el), reverse=True)
    num_solutions = []
    for i, pattern in enumerate(patterns):
        sols = find_num_solutions(pattern)
        print(i, sols)
        num_solutions.append(sols)
    print(sum(bool(s) for s in num_solutions))
    print(sum(num_solutions))

if __name__ == "__main__":
    main()
