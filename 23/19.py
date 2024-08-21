from dataclasses import dataclass


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    accepted: bool = False


@dataclass
class PartRange:
    xmin: int = 1
    xmax: int = 4000
    mmin: int = 1
    mmax: int = 4000
    amin: int = 1
    amax: int = 4000
    smin: int = 1
    smax: int = 4000

    def split(self, cond) -> tuple["PartRange", "PartRange"]:
        """Returns (false, true)"""
        if cond == "True":
            return None, self
        out = (
            PartRange(
                xmin=self.xmin,
                xmax=self.xmax,
                mmin=self.mmin,
                mmax=self.mmax,
                amin=self.amin,
                amax=self.amax,
                smin=self.smin,
                smax=self.smax,
            ),
            PartRange(
                xmin=self.xmin,
                xmax=self.xmax,
                mmin=self.mmin,
                mmax=self.mmax,
                amin=self.amin,
                amax=self.amax,
                smin=self.smin,
                smax=self.smax,
            ),
        )
        swap = cond[1] == "<"
        val = int(cond[2:])
        setattr(out[0], cond[0] + "max", val - swap)
        setattr(out[1], cond[0] + "min", val + (not swap))
        if swap:
            out = (out[1], out[0])
        if out[0].invalid or out[1].invalid:
            return self, None
        return out

    @property
    def invalid(self) -> bool:
        return not all(
            getattr(self, i + "max") >= getattr(self, i + "min") for i in "xmas"
        )

    def __len__(self) -> int:
        if self.invalid:
            return 0
        return (
            (self.xmax - self.xmin + 1)
            * (self.mmax - self.mmin + 1)
            * (self.amax - self.amin + 1)
            * (self.smax - self.smin + 1)
        )


class Workflow:
    def __init__(self, recipe: str):
        self.conditions = []
        conditions = recipe.split(",")
        for cond in conditions[:-1]:
            self.conditions.append(cond.split(":"))
        self.conditions.append(["True", conditions[-1]])

    def __call__(self, param: Part):
        x, m, a, s = param.x, param.m, param.a, param.s
        for cond in self.conditions:
            if eval(cond[0]):
                return cond[1]

    def __str__(self) -> str:
        return (
            "Workflow(\n\t"
            + "\n\t".join(f"{c[0]}: {c[1]}" for c in self.conditions)
            + "\n)"
        )


def explore_workflow(workflows, workflow, ranges):
    if ranges is None:
        return 0
    res = 0
    for cond, key in workflow.conditions:
        ranges, passing_ranges = ranges.split(cond)
        if passing_ranges is None or key == "R":
            continue
        if key == "A":
            res += len(passing_ranges)
        else:
            res += explore_workflow(workflows, workflows[key], passing_ranges)
    return res


def main():
    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []

    with open("19", "r") as f:
        # Workflows
        for line in f:
            if not line.strip():
                break
            key, recipe = line.strip()[:-1].split("{")
            workflows[key] = Workflow(recipe)
        # Parts
        for line in f:
            exec(f"parts.append(Part({line.strip()[1:-1]}))")

    for part in parts:
        key = "in"
        while key not in "AR":
            key = workflows[key](part)
        if key == "A":
            part.accepted = True

    print(sum(p.x + p.m + p.a + p.s for p in parts if p.accepted))

    print(explore_workflow(workflows, workflows["in"], PartRange()))


if __name__ == "__main__":
    main()
