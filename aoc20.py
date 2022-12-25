
fasit = iter([
    [2, 1, -3, 3, -2, 0, 4],
    [1, -3, 2, 3, -2, 0, 4],
    [1, 2, 3, -2, -3, 0, 4],
    [1, 2, -2, -3, 0, 3, 4],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 4, 0, 3, -2]
])

with open("input20.txt", "r") as f:
    data = [int(l) for l in f]

l = len(data)

for n in data.copy():
    i = data.index(n)
    if n < 0:
        data = data[i:] + data[:i]
        data.append(data.pop(0))

        data[n-1:] = [n] + data[n-1:-1]

    elif n > 0:
        data = data[i:] + data[:i]   

        data[:n+1] = data[1:n+1] + [n]

    # el = next(fasit)
    # while data[0] != el[0]:
    #     data.append(data.pop(0))
    # print("sort")
    # print(data)
    # print(el)
    # print()
        
ind = data.index(0)
ans = [data[(ind + i) % l] for i in [1000, 2000, 3000]]
print(ans)
print(sum(ans))
