
def main():

    n = 0
    max_n = 0
    max_cal = 0
    cal = 0
    skips = [30, 159]
    with open("input01.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                cal += int(line)
            else:
                if cal > max_cal and n not in skips:
                    max_cal = cal
                    max_n = n
                cal = 0
                n += 1
    
    print(max_n, max_cal)
    print(66306 + 64532 + 64454)

if __name__ == "__main__":
    main()

