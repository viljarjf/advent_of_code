
with open("input20.txt", "r") as f:
    data = [l.strip() for l in f]
counts = {}
for i, l in enumerate(data):
    count = counts.get(l, 0)
    data[i] += f"|{count}"
    counts[l] = count + 1

l = len(data)
# print(len(set(data)))
# fuck me, the elements are not unique
# I need another way to get i below
og = data.copy()
def mix(data):
    for n in og:
        i = data.index(n) 
        _n = n
        n = (int(n.split("|")[0]) % (l - 1))

        if n < 0:
            data = data[i:] + data[:i]
            data.append(data.pop(0))
            data[n-1:] = [_n] + data[n-1:-1]

        elif n > 0:
            data = data[i:] + data[:i]   
            data[:n+1] = data[1:n+1] + [_n]

        i = data.index("0|0")
        data = data[i:] + data[:i]
        data.append(data.pop(0))
        data.append(data.pop(0))
        data.append(data.pop(0))
        data.append(data.pop(0))
    return data
data = mix(data)
ind = data.index("0|0")
ans = [data[(ind + i) % l] for i in [1000, 2000, 3000]]

print(ans)
print(sum(int(i.split("|")[0]) for i in ans))

og = [str(811589153 * int(i.split("|")[0])) + "|" + i.split("|")[1] for i in og]
data = og.copy()
for _ in range(10):
    print(_)
    data = mix(data)
ind = data.index("0|0")
ans = [data[(ind + i) % l] for i in [1000, 2000, 3000]]

print(ans)
print(sum(int(i.split("|")[0]) for i in ans))
