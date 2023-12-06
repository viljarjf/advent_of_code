from __future__ import annotations
from typing import TextIO, Iterable


class MapRange:
    def __init__(self, dst: int, src: int, size: int):
        self.dst = dst
        self.src = src
        self.size = size
        self.range = range(src, src + size)

    def __contains__(self, item: int) -> bool:
        return item in self.range

    def __getitem__(self, ind: int) -> int:
        return self.dst + (ind - self.src)


class Map:
    def __init__(self):
        self.ranges: list[MapRange] = []

    def __getitem__(self, ind: int) -> int:
        for range in self.ranges:
            if ind in range:
                return range[ind]
        return ind

    def add_range(self, dst: int, src: int, size: int):
        self.ranges.append(MapRange(dst, src, size))

    def get_break_points(self) -> list[int]:
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

    def reverse(self) -> MapSequence:
        reversed_maps = []
        for map in reversed(self.maps):
            new_map = Map()
            for range in map.ranges:
                new_map.add_range(range.src, range.dst, range.size)
            reversed_maps.append(new_map)
        return MapSequence(reversed_maps)

    def get_break_points(self) -> list:
        points = []
        for m in self.reverse().maps:
            points += m.get_break_points()
            points = [m[p] for p in points]
        return points


def get_map(inp: TextIO) -> Map:
    m = Map()
    while line := inp.readline().strip():
        dst, src, l = line.split(" ")
        dst, src, l = int(dst), int(src), int(l)
        m.add_range(dst, src, l)
    return m


def main():
    with open("05", "r", encoding="utf-8") as inp:
        seeds = [int(i) for i in inp.readline().split(":")[1].strip().split(" ")]

        inp.readline()  # empty

        maps = []

        while inp.readline().strip():
            maps.append(get_map(inp))
        maps = MapSequence(maps)

    locs = []
    for seed in seeds:
        locs.append(maps[seed])
    print(min(locs))

    seed_ranges = [
        range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]
    reverse_maps = maps.reverse()
    locs = []
    for loc in reverse_maps.get_break_points():
        seed = reverse_maps[loc]
        if any(seed in sr for sr in seed_ranges):
            locs.append(loc)

    print(min(locs))

if __name__ == "__main__":
    main()
