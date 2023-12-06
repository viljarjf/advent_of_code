with open("input04.txt", "r") as f:
    data = [i for i in f]

n = 0
m = 0
for d in data:
    a, b = d.strip().split(",")
    a1, a2 = a.split("-")
    b1, b2 = b.split("-")
    a1 = int(a1)
    a2 = int(a2)
    b1 = int(b1)
    b2 = int(b2)

    if a1 <= b1 and a2 >= b2:
        n += 1
        m += 1
    elif b1 <= a1 and b2 >= a2:
        n += 1
        m += 1
    elif a2 >= b1 and a1 <= b2:
        m += 1
    elif b2 >= a1 and b1 <= a2:
        m += 1
    
print(n)
print(m)
