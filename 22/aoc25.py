
snafu = {
    "0": 0,
    "1": 1,
    "2": 2,
    "-": -1,
    "=": -2
}

ufans = {
    0: "0",
    1: "1",
    2: "2",
    -1: "-",
    -2: "="
}

with open("input", "r") as f:
    s = 0
    for l in f:
        p = 1
        for char in l.strip()[::-1]:
            s += p * snafu[char]
            p *= 5
print(s)

# convert to base 5
s_5 = []
while s:
    s, rem = divmod(s, 5)
    s_5.append(rem)
s_5.append(0)
# 04 -> 1-
# 03 -> 1=
print(s_5)
for i in range(len(s_5)):
    if s_5[i] > 2:
        s_5[i] -= 5
        s_5[i + 1] += 1

print(s_5)
print("".join(ufans[i] for i in s_5[::-1]))

