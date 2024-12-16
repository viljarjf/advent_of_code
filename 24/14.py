class Robot:

    def __init__(self, s: str, testing: bool = False):
        p, v = s.strip().split()
        p0, p1 = p[2:].split(",")
        v0, v1 = v[2:].split(",")
        self.p = (int(p0), int(p1))
        self.v = (int(v0), int(v1))
        self.bounds = (11, 7) if testing else (101, 103)

    def move(self, t: int) -> tuple[int, int]:
        return (
            (self.p[0] + t * self.v[0]) % self.bounds[0],
            (self.p[1] + t * self.v[1]) % self.bounds[1],
        )
    
    def get_quadrant_after(self, t: int) -> int | None:
        x, y = self.move(t)
        xm = self.bounds[0] // 2
        ym = self.bounds[1] // 2
        if x > xm and y > ym:
            return 0
        if x < xm and y > ym:
            return 1
        if x < xm and y < ym:
            return 2
        if x > xm and y < ym:
            return 3
        return None


def get_robots(testing: bool = False) -> list[Robot]:
    with open("14_test" if testing else "14", "r") as f:
        return [Robot(line, testing) for line in f]

def interactive_plot(robots: list[Robot], init: int = 0):
    import matplotlib
    matplotlib.use("qtagg")

    from matplotlib import pyplot as plt
    plt.figure()

    import numpy as np
    def get_robot_positions(t: int) -> np.ndarray:
        arr = np.zeros(robots[0].bounds, dtype=int)
        for r in robots:
            arr[r.move(t)] += 1
        return arr.T

    img = plt.imshow(get_robot_positions(init))

    plt.axis("off")
    plt.subplots_adjust(bottom=0.25)

    from matplotlib.widgets import Slider
    slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider = Slider(
        ax=slider_ax,
        label='t',
        valmin=0,
        valmax=10403,
        valinit=init,
    )

    def on_changed(arg):
        img.set_data(get_robot_positions(int(slider.val)))
    
    slider.on_changed(on_changed)

    plt.show()


def main():
    robots = get_robots()
    quadrant_count = [0, 0, 0, 0]
    for robot in robots:
        q = robot.get_quadrant_after(100)
        if q is not None:
            quadrant_count[q] += 1
    print(quadrant_count[0] * quadrant_count[1] * quadrant_count[2] * quadrant_count[3])

    # Both 11, 7, 101, and 103 are prime
    # Therefore, the period is just 11*7 or 101*103
    period = robots[0].bounds[0] * robots[0].bounds[1]
    for t in range(period):
        p = [r.move(t) for r in robots]
        if len(p) == len(set(p)):
            print(t)

    interactive_plot(robots, 7572)

if __name__ == "__main__":
    main()
