from __future__ import annotations
from typing import TextIO, Iterable

class Map:

    class Range:
        def __init__(self, dst: int, src: int, size: int):
            self.dst = dst
            self.src = src
            self.size = size
            self.range = range(src, src + size)

        def __contains__(self, item: int) -> bool:
            return item in self.range

        def __getitem__(self, ind: int) -> int:
            return self.dst + (ind - self.src)

    @classmethod
    def from_file(cls, inp: TextIO) -> Map:
        m = cls()
        while line := inp.readline().strip():
            dst, src, l = line.split(" ")
            dst, src, l = int(dst), int(src), int(l)
            m.add_range(dst, src, l)
        return m

    def __init__(self):
        self.ranges: list[self.Range] = []

    def __getitem__(self, ind: int) -> int:
        for r in self.ranges:
            if ind in r:
                return r[ind]
        return ind

    def add_range(self, dst: int, src: int, size: int):
        self.ranges.append(self.Range(dst, src, size))

    def get_break_points(self) -> list[int]:
        """
        Get a list of possible break points, 
        i.e. points where the difference between values at consecutive indices are not 1. 
        The list will always contain all break points, 
        but will also contain points which are not.
        """
        points = []
        for r in self.ranges:
            points += [
                r.src,
                r.src + r.size,
                r.dst,
                r.dst + r.size,
                r.src - 1,
                r.src + r.size - 1,
                r.dst + 1,
                r.dst + r.size + 1,
                r.src + 1,
                r.src + r.size + 1,
                r.dst + 1,
                r.dst + r.size + 1,
            ]
        return points

class MapSequence:
    def __init__(self, maps: Iterable[Map]):
        self.maps = maps

    def __getitem__(self, ind: int) -> int:
        for map in self.maps:
            ind = map[ind]
        return ind

    def reversed(self) -> MapSequence:
        reversed_maps = []
        for map in reversed(self.maps):
            new_map = Map()
            for range in map.ranges:
                new_map.add_range(range.src, range.dst, range.size)
            reversed_maps.append(new_map)
        return MapSequence(reversed_maps)

    def get_break_points(self) -> list:
        """
        Get a list of possible break points, 
        i.e. points where the difference between values at consecutive indices are not 1. 
        The list will always contain all break points, 
        but will also contain points which are not.
        """
        points = []
        for m in self.reversed().maps:
            points += m.get_break_points()
            points = [m[p] for p in points]
        return points


def main():
    with open("05", "r", encoding="utf-8") as inp:
        seeds = [int(i) for i in inp.readline().split(":")[1].strip().split(" ")]

        inp.readline()  # empty

        maps = []
        while inp.readline().strip():
            maps.append(Map.from_file(inp))

    maps = MapSequence(maps)

    locs = []
    for seed in seeds:
        locs.append(maps[seed])
    print(min(locs))

    seed_ranges = [
        range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]
    reverse_maps = maps.reversed()
    locs = []
    for loc in reverse_maps.get_break_points():
        seed = reverse_maps[loc]
        if any(seed in sr for sr in seed_ranges):
            locs.append(loc)

    print(min(locs))

if __name__ == "__main__":
    main()
