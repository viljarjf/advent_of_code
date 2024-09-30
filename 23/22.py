import heapq

class Brick:
    def __init__(self, desc: str):
        start, end = desc.strip().split("~")
        x0, y0, z0 = start.split(",")
        x1, y1, z1 = end.split(",")
        x0, y0, z0 = int(x0), int(y0), int(z0)
        x1, y1, z1 = int(x1), int(y1), int(z1)
        self.x0, x1 = min(x0, x1), max(x0, x1)
        self.y0, y1 = min(y0, y1), max(y0, y1)
        self.z0, z1 = min(z0, z1), max(z0, z1)
        self.dx = x1 - self.x0 + 1
        self.dy = y1 - self.y0 + 1
        self.dz = z1 - self.z0 + 1
        self.above: set[Brick] = set()
        self.below: set[Brick] = set()
    
    @property
    def x1(self) -> int:
        return self.x0 + self.dx - 1
    
    @property
    def y1(self) -> int:
        return self.y0 + self.dy - 1
    
    @property
    def z1(self) -> int:
        return self.z0 + self.dz - 1
    
    @property
    def x(self) -> range:
        return range(self.x0, self.x1 + 1)
    
    @property
    def y(self) -> range:
        return range(self.y0, self.y1 + 1)
    
    @property
    def z(self) -> range:
        return range(self.z0, self.z1 + 1)

    @property
    def coords(self) -> set[tuple[int, int, int]]:
        return set((x, y, z) for x in self.x for y in self.y for z in self.z)
    
    @property
    def xy_coords(self) -> set[tuple[int, int]]:
        return set((x, y) for x in self.x for y in self.y)

    @property
    def desc(self) -> str:
        return f"{self.x0},{self.y0},{self.z0}~{self.x1},{self.y1},{self.z1}"

    def copy(self) -> "Brick":
        return Brick(self.desc)

    def __eq__(self, other: "Brick") -> bool:
        if isinstance(other, Brick):
            return (
                self.x0 == other.x0
                and self.y0 == other.y0
                and self.z0 == other.z0
                and self.x1 == other.x1
                and self.y1 == other.y1
                and self.z1 == other.z1
            )
        return NotImplemented

    def __lt__(self, other: "Brick"):
        return self.z0 < other.z0

    def __str__(self):
        return f"{self.__class__.__name__}(x = {(
                self.x0, self.x1
            )}, y = {(
                self.y0, self.y1
            )}, z = {(
                self.z0, self.z1
            )})"

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return hash(self.desc)

    def is_above(self, other: "Brick") -> bool:
        if self.z0 <= other.z1:
            return False
        return not self.xy_coords.isdisjoint(other.xy_coords)

    def drop(self, bricks: list["Brick"]) -> "Brick":
        candidates = [b for b in bricks if self.is_above(b)]
        if len(candidates) == 0:
            self.z0 = 1
        else:
            z = max(b.z1 for b in candidates)
            self.z0 = z + 1
        return self


def _lower(bricks: list[Brick]) -> list[Brick]:
    fallen_bricks: list[Brick] = []
    sliced_bricks = slice_bricks(bricks)
    for s in sliced_bricks:
        for brick in s:
            brick.drop(fallen_bricks)
        fallen_bricks += s
    # link
    for above in fallen_bricks:
        for below in fallen_bricks:
            if below.z1 == above.z0 - 1 and above.is_above(below):
                below.above.add(above)
                above.below.add(below)

    # Check for any intersections, just in case
    # coords = sum([list(b.coords) for b in bricks], start=[])
    # assert len(coords) == len(set(coords))

    # Check links
    # for brick in fallen_bricks:
    #     for above in brick.above:
    #         assert brick in above.below
    #         assert above.z0 == brick.z1 + 1
    #     for below in brick.below:
    #         assert brick.is_above(below)
    #         assert below.z1 == brick.z0 - 1
    return fallen_bricks

def all_coords(bricks: list[Brick]) -> dict[tuple[int, int, int], Brick]:
    return {coord : brick for brick in bricks for coord in brick.coords}

def lower(bricks: list[Brick]) -> None:
    bricks = [b.copy() for b in bricks]
    for z0 in range(max(b.z1 for b in bricks) + 1):
        for brick in bricks:
            if brick.z0 == z0:
                coords = all_coords(bricks)
                while brick.z0 > 1:
                    for x, y, z in brick.coords:
                        other = coords.get((x, y, z -1))
                        if other is not None and other is not brick:
                            break
                    else:
                        brick.z0 -= 1
                        continue
                    break
    # establish connection
    for brick in bricks:
        for x, y, z in brick.coords:
            if (below := coords.get((x, y, z - 1))) is not None:
                below.above.add(brick)
                brick.below.add(below)
            if (above := coords.get((x, y, z + 1))) is not None:
                above.below.add(brick)
                brick.above.add(above)
    return bricks


def slice_bricks(bricks: list[Brick]) -> list[list[Brick]]:
    out = []
    for z in range(max(brick.z1 for brick in bricks)):
        out.append([brick.copy() for brick in bricks if brick.z0 == z])
    return out

def slice_bricks_no_copy(bricks: list[Brick]) -> list[list[Brick]]:
    out = []
    for z in range(max(brick.z1 for brick in bricks)):
        out.append([brick for brick in bricks if brick.z0 == z])
    return out

def count_safe_bricks(bricks: list[Brick]) -> int:
    tot = 0
    for brick in bricks:
        if all(len(above.below) > 1 for above in brick.above):
            tot += 1
    return tot

def get_supported_bricks(brick: Brick) -> list[Brick]:
    queue = [brick]
    out = [brick]
    while queue:
        b = queue.pop(0)
        for above in b.above:
            if above in out:
                continue
            out.append(above)
            queue.append(above)
    return out

def count_chain(bricks: list[Brick]) -> int:
    tot = 0
    for brick in bricks:
        supported_bricks = get_supported_bricks(brick)
        for supported in supported_bricks[1:]:
            # Check if any supported bricks are also supported by some other brick
            if any(b not in supported_bricks for b in supported.below):
                # Purge the tree
                for doubly_supported in get_supported_bricks(supported):
                    if doubly_supported in supported_bricks:
                        supported_bricks.remove(doubly_supported)
        tot += len(supported_bricks) - 1
    return tot

def get_bricks(filename: str) -> list[Brick]:
    with open(filename, "r") as f:
        return [Brick(line) for line in f]


def main():
    bricks = get_bricks("22")
    b = bricks[0]
    # for b in bricks:
    #     print(b)
    print("-" * len(str(b)))
    bricks = lower(bricks)
    # bricks = sorted(bricks)
    # for b in bricks:
    #     print(b)
    supports = [len(b.below) for b in bricks]
    for i in range(max(supports)):
        print(f"{i} supports: {supports.count(i)}")
    print("-" * len(str(b)))
    supporting = [len(b.above) for b in bricks]
    for i in range(max(supporting)):
        print(f"supporting {i}: {supporting.count(i)}")
    print("-" * len(str(b)))
    print(f"{count_safe_bricks(bricks)} / {len(bricks)}")
    print("-" * len(str(b)))
    print(count_chain(bricks))


def test():
    a = Brick("0,0,1~0,5,1")
    assert not a.is_above(a)

    # parallel, same height
    b = Brick("1,0,1~1,5,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # parallel, different height
    b = Brick("1,0,4~1,5,6")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # parallel, no intersection, same height
    b = Brick("0,10,1~0,15,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # parallel, no intersection, different height
    b = Brick("0,10,10~0,15,10")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # parallel, intersection, same height
    b = Brick("0,2,1~0,15,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # parallel, intersection, different height
    b = Brick("0,2,10~0,15,10")
    assert not a.is_above(b)
    assert b.is_above(a)

    # parallel, contained, same height
    b = Brick("0,2,1~0,3,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # parallel, contained, different height
    b = Brick("0,2,10~0,3,10")
    assert not a.is_above(b)
    assert b.is_above(a)

    # cross, no lineup, same height
    b = Brick("7,7,1~10,7,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # cross, no lineup, different height
    b = Brick("7,7,10~10,7,10")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # cross, lineup, same height
    b = Brick("7,3,1~10,3,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # cross, lineup, different height
    b = Brick("7,3,10~10,3,10")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # true cross, same height
    b = Brick("0,3,1~10,3,1")
    assert not a.is_above(b)
    assert not b.is_above(a)

    # true cross, different height
    b = Brick("0,3,10~10,3,10")
    assert not a.is_above(b)
    assert b.is_above(a)

    bricks = get_bricks("22_test")
    bricks = lower(bricks)
    assert count_safe_bricks(bricks) == 5
    # assert count_chain_old(bricks) == 7
    # assert count_chain(bricks) == 7

    old_bricks = [b.copy() for b in bricks]
    for b in bricks:
        b.z0 += 4 + b.z1 * 3
    assert all(b1 == b2 for b1, b2 in zip(lower(bricks), old_bricks))

    assert all(b1 == b2 for b1, b2 in zip(lower(bricks), lower(lower(bricks))))

    bricks = get_bricks("22_test")
    assert set(lower(bricks)) == set(lower(lower(lower(bricks))))
    bricks = get_bricks("22")
    assert set(lower(bricks)) == set(lower(lower(lower(bricks))))

    bricks = get_bricks("22")
    assert set(lower(bricks)) == set(_lower(bricks))


if __name__ == "__main__":
    # test()
    main()
    # Idk man, the 1st task needs Brick._lower and the 2nd task needs Brick.lower
