
def main():
    with open("input02.txt", "r") as f:
        score0 = 0
        score1 = 0
        s = [0, "X", "Y", "Z"]
        s1 = ["A", "B", "C"]
        for line in f:
            a,b = line.split()
            if (a == "A" and b == "Y") or (a == "B" and b == "Z") or (a == "C" and b == "X"):
                score0 += 6
            if (a == "A" and b == "X") or (a == "B" and b == "Y") or (a == "C" and b == "Z"):
                score0 += 3
            score0 += s.index(b)

            if b == "X":
                score1 += s1.index(chr((ord(a) - ord("A")-1) % 3 + ord("A"))) + 1
            elif b == "Y":
                score1 += s1.index(a) + 1 + 3
            elif b == "Z":
                score1 += s1.index(chr((ord(a) - ord("A")+1) % 3 + ord("A"))) + 1 + 6

        print(score0)
        print(score1)
if __name__ == "__main__":
    main()
