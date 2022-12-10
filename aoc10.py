x = 1
c = 0
s = 0
width = 40

with open("input10.txt", "r") as f:
    line = ""
    for l in f:
        for _ in range(len(l.strip().split())):
            # draw
            if abs(c % width - x) <= 1:
                line += "#"
            else:
                line += "."

            # clock
            c += 1

            # task 1
            if not (c - 20) % width:
                s += c*x

            # new line
            if not c % width:
                line += "\n"

            # noop
            if l.strip() == "noop":
                break
        # incx
        else:
            x += int(l.split()[1])    

    print(s)
    print(line)
