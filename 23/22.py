import numpy as np

class Brick:
    def __init__(self, desc: str):
        self.desc = desc
        start, end = desc.strip().split("~")
        x0, y0, z0 = start.split(",")
        x1, y1, z1 = end.split(",")
        x0, y0, z0 = int(x0), int(y0), int(z0)
        x1, y1, z1 = int(x1), int(y1), int(z1)
        self.x0, self.x1 = min(x0, x1), max(x0, x1)
        self.y0, self.y1 = min(y0, y1), max(y0, y1)
        self.z0, self.z1 = min(z0, z1), max(z0, z1)
        self.x = range(self.x0, self.x1 + 1)
        self.y = range(self.y0, self.y1 + 1)
        self.z = range(self.z0, self.z1 + 1)
        self.dx = self.x1 - self.x0
        self.dy = self.y1 - self.y0
        self.dz = self.z1 - self.z0

    def copy(self) -> "Brick":
        return Brick(self.desc)
    
    def __eq__(self, other) -> bool:
        return (
            self.x0 == other.x0 and
            self.y0 == other.y0 and
            self.z0 == other.z0 and
            self.x1 == other.x1 and
            self.y1 == other.y1 and
            self.z1 == other.z1
        )

    def __lt__(self, other: "Brick"):
        return self.z0 < other.z0

    def __str__(self):
        return f"{self.__class__.__name__}(x = ({self.x0}, {self.x1}), y = ({self.y0}, {self.y1}), z = ({self.z0}, {self.z1})) "
    
    def __repr__(self): 
        return str(self)
    
    def is_intersecting_xy(self, other: "Brick") -> bool:
        for x in self.x:
            for y in self.y:
                if x in other.x and y in other.y:
                    return True
        return False
    
    def drop(self, bricks: list["Brick"]) -> "Brick":
        if self.z0 == 1:
            return self
        self.z0 = 1
        self.z1 = self.z0 + self.dz
        for brick in bricks:
            if self.is_intersecting_xy(brick):
                self.z0 = brick.z0 + 1
                self.z1 = self.z0 + self.dz
        return self

def lower(bricks: list[Brick]) -> None:
    for i, brick in enumerate(bricks):
        brick.drop(bricks[:i])

def count_safe_bricks(bricks: list[Brick]) -> int:
    count = 0
    for i in range(len(bricks)):
        print("---")
        print(bricks[i])
        for brick in bricks[i+1:]:
            z = brick.z0
            if brick.copy().drop(bricks[:i]).z0 != z:
                count += 1
                print(brick)
                print(brick.copy().drop(bricks[:i]))
                print()
                break
    return len(bricks) - count

def main():
    bricks = []
    with open("22_test", "r") as f:
        for line in f:
            bricks.append(Brick(line))
    
    bricks = sorted(bricks)
    lower(bricks)
    print(bricks)
    print(count_safe_bricks(bricks))

if __name__ == "__main__":
    main()
