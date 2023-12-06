with open("input03.txt", "r") as f:
    data = [i for i in f]

p = "abcdefghijklmnopqrstuvwxyz"
p = "_" + p + p.upper()

score = 0
for d in data:
    c1 = d[:len(d)//2]
    c2 = d[len(d)//2:]
    for i in c1:
        if i in c2:
            score += p.index(i)
            break

print(score)

score = 0
for i in range(0, len(data)-1, 3):
    d1 = data[i]
    d2 = data[i+1]
    d3 = data[i+2]

    for c in d1.strip():
        if c in d2 and c in d3:
            score += p.index(c)
            break
print(score)
