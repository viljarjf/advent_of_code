import yaml

with open("input11.txt", "r") as f:
    c = f.read().replace("  If true", "pass").replace("  If false", "fail")

data = yaml.load(c, yaml.Loader)

def main(rounds: int, divisor: int) -> int:
    monkeys = []
    for m in data.values():
        d = dict()
        d["i"] = [int(i) for i in str(m["Starting items"]).split(",")]
        d["_o"] = eval("lambda old:" + m["Operation"][5:])
        p = int(m["pass"].split()[-1])
        f = int(m["fail"].split()[-1])
        m = int(m["Test"].split()[-1])
        d["t"] = (lambda true, false, test: lambda n: false if n % test else true)(p, f, m)
        d["m"] = m
        d["n"] = 0
        monkeys.append(d)

    mod = 1
    for m in monkeys:
        mod *= m["m"]
    for m in monkeys:
        m["o"] = lambda n: m["_o"](n) % mod

    for _ in range(rounds):
        for m in monkeys:
            while m["i"]:
                i = m["i"].pop()
                i = m["o"](i)
                i //= divisor
                monkeys[m["t"](i)]["i"].append(i)
                m["n"] += 1
        # for m in monkeys:
        #     print(m["n"])
        # print()


    return max([m["n"] for m in monkeys]) * sorted([m["n"] for m in monkeys])[-2]
  
print(main(20, 3))
print(main(10000,1))
