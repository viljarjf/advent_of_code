from numpy import lcm, uint64

def main():

    with open("08", "r", encoding="utf-8") as inp:
        instructions = inp.readline().strip()
        inp.readline() # empty

        map = dict()
        for line in inp:
            key, val = line.split("=")
            key, val = key.strip(), val.strip()
            map[key] = tuple(val[1:-1].split(", "))

    step = 0
    key = "AAA"
    while key != "ZZZ":
        ins = instructions[step % len(instructions)] == "R"
        key = map[key][ins]
        step += 1
    
    print(step)

    step = 0
    keys = [key for key in map.keys() if key[-1] == "A"]
    cycle_length = [-1 for _ in keys]
    while any(cycle == -1 for cycle in cycle_length):
        for i, key in enumerate(keys):
            if key[-1] == "Z" and cycle_length[i] < 0:
                cycle_length[i] = step
        ins = instructions[step % len(instructions)] == "R"
        for i, key in enumerate(keys):
            keys[i] = map[key][ins]
        step += 1
    
    # Note: int32 is too small, gave wrong answer.
    print(lcm.reduce(cycle_length, dtype=uint64))

if __name__ == "__main__":
    main()
