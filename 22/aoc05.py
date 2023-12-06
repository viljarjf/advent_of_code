with open("input05.txt", "r") as f:
    data = [i for i in f]
    data = data[10:]

crates = [
    ["V", "J", "B", "D"],
    ["F", "D", "R", "W", "B", "V", "P"],
    ["Q","W","C","D","L","F","G","R"],
    ["B", "D", "N", "L", "M", "P", "J", "W"],
    ["Q", "S", "C", "P", "B", "N", "H"],
    ["G", "N", "S", "B", "D", "R"],
    ["H", "S", "F", "Q", "M", "P", "B", "Z"],
    ["F", "L", "W"],
    ["R", "M", "F", "V", "S"]
]
crates2 = [
    ["V", "J", "B", "D"],
    ["F", "D", "R", "W", "B", "V", "P"],
    ["Q","W","C","D","L","F","G","R"],
    ["B", "D", "N", "L", "M", "P", "J", "W"],
    ["Q", "S", "C", "P", "B", "N", "H"],
    ["G", "N", "S", "B", "D", "R"],
    ["H", "S", "F", "Q", "M", "P", "B", "Z"],
    ["F", "L", "W"],
    ["R", "M", "F", "V", "S"]
]

for l in data:
    d = l.split()
    n = int(d[1])
    i = int(d[3]) - 1
    f = int(d[5]) - 1
    for _ in range(n):
        crates[f].insert(0, crates[i].pop(0))
    crates2[f] = crates2[i][:n] + crates2[f]
    crates2[i][:n] = []
    pass

print("".join(i[0] for i in crates))
print("".join(i[0] for i in crates2))