from itertools import combinations
import sympy

class Hail:

    def __init__(self, inp: str) -> None:
        pos, vel = inp.strip().split("@")
        self.x0, self.y0, self.z0 = [int(i.strip()) for i in pos.split(",")]
        self.vx, self.vy, self.vz = [int(i.strip()) for i in vel.split(",")]
    
    @property
    def r0(self) -> tuple[int, int, int]:
        return (self.x0, self.y0, self.z0)
    
    @property
    def v(self) -> tuple[int, int, int]:
        return (self.vx, self.vy, self.vz)
    
    def x(self, t: float) -> float:
        return self.x0 + self.vx * t
    
    def y(self, t: float) -> float:
        return self.y0 + self.vy * t
    
    def z(self, t: float) -> float:
        return self.z0 + self.vz * t
    
    def r(self, t: float) -> tuple[float, float, float]:
        return (self.x(t), self.y(t), self.z(t))
    
    def t(self, pos: tuple[float, float, float]) -> float | None:
        xt = (pos[0] - self.x0) / self.vx
        yt = (pos[1] - self.y0) / self.vy
        zt = (pos[2] - self.z0) / self.vz
        delta = abs(xt - yt) + abs(xt - zt) + abs(yt - zt)
        if delta > 0.5:
            return None
        return xt
    
    def t_xy(self, pos: tuple[float, float]) -> float:
        xt = (pos[0] - self.x0) / self.vx
        # yt = (pos[1] - self.y0) / self.vy
        return xt
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(r0 = {self.r0}, v = {self.v})"
    
    def __repr__(self) -> str:
        return str(self)
    
def find_intersection_xy(a: Hail, b: Hail) -> tuple[float, float] | None:
    den = a.vx * b.vy - a.vy * b.vx
    if den == 0:
        return None
    x1, x2 = a.x(0), a.x(1)
    y1, y2 = a.y(0), a.y(1)
    x3, x4 = b.x(0), b.x(1)
    y3, y4 = b.y(0), b.y(1)
    num_x = (x1 * y2 - y1 * x2) * (-b.vx) - (-a.vx) * (x3 * y4 - y3 * x4)
    num_y = (x1 * y2 - y1 * x2) * (-b.vy) - (-a.vy) * (x3 * y4 - y3 * x4)
    pos = (num_x / den, num_y / den)
    if a.t_xy(pos) < 0:
        return None
    if b.t_xy(pos) < 0:
        return None
    return pos

def get_intersecting_hail(hails: list[Hail]) -> Hail:
    # Just sit down with a pen and paper and write it out
    # OR make sympy solve it.
    # Pen and paper helped, at least:
    # The system is overdetermined, so we only need three hails
    h1, h2, h3 = hails[:3]
    rx, ry, rz = sympy.symbols("rx, ry, rz")
    vx, vy, vz = sympy.symbols("vx, vy, vz")
    t1, t2, t3 = sympy.symbols("t1, t2, t3")
    eqs = [
        sympy.Eq(rx + vx * t1, h1.r(t1)[0]),
        sympy.Eq(rx + vx * t2, h2.r(t2)[0]),
        sympy.Eq(rx + vx * t3, h3.r(t3)[0]),
        sympy.Eq(ry + vy * t1, h1.r(t1)[1]),
        sympy.Eq(ry + vy * t2, h2.r(t2)[1]),
        sympy.Eq(ry + vy * t3, h3.r(t3)[1]),
        sympy.Eq(rz + vz * t1, h1.r(t1)[2]),
        sympy.Eq(rz + vz * t2, h2.r(t2)[2]),
        sympy.Eq(rz + vz * t3, h3.r(t3)[2]),
    ]
    sol, = sympy.solve(eqs)
    return Hail(f"{sol[rx]}, {sol[ry]}, {sol[rz]} @ {sol[vx]}, {sol[vy]}, {sol[vz]}")

def get_hail(filename: str) -> list[Hail]:
    with open(filename, "r") as f:
        return [Hail(line) for line in f]

def main():
    hails = get_hail("24")
    lower = 200000000000000
    upper = 400000000000000
    crossings = 0
    for a, b in combinations(hails, 2):
        inter = find_intersection_xy(a, b)
        if inter is None:
            continue
        x, y = inter
        if lower <= x <= upper and lower <= y <= upper:
            crossings += 1
    print(crossings)

    h = get_intersecting_hail(hails)
    print(h.x0 + h.y0 + h.z0)

if __name__ == "__main__":
    main()
