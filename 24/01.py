with open("01", "r") as f:
    lines = (line.strip() for line in f)
    a, b = zip(*(line.split("   ") for line in lines))
    a = (int(i) for i in a)
    b = (int(i) for i in b)
    a = sorted(a)
    b = sorted(b)
    diff = (abs(ai - bi) for ai, bi in zip(a, b))
    print(sum(diff))
    c = {i : b.count(i) for i in set(b)}
    print(sum(i * c.get(i, 0) for i in a))
    