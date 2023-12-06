with open("input06.txt", "r") as f:
    d = [i for i in f][0]
    for l in [4, 14]:
        for i in range(l-1, len(d)):
            s = d[i-l:i]
            if len(set([c for c in s])) == l:
                print(i)
                break
