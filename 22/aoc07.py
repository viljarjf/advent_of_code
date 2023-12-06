dirs = dict()
cwd = ""

d = dict()
stack = []

# parse
with open("input07.txt", "r") as f:
    for l in f:
        match l.split():
            case ["$", "cd", dir]:
                if dir == "..":
                    _d = d
                    d, dir = stack.pop()
                    d[dir].update(_d)
                else:
                    cwd = dir
                    stack.append((d, cwd))
                    d = dict()
            case ["$", "ls"]:
                pass
            case ["dir", dir]:
                d[dir] = dict()
            case [size, filename]:
                d[filename] = int(size)

while len(stack) > 1:
    _d = d
    d, dir = stack.pop()
    d[dir].update(_d)     
  
_d = d
d, dir = stack.pop()
dirs[dir] = _d


# calculate size
sumkey = "__sum"

def calc_score(d: dict):
    score = 0
    if d.get(sumkey) is None:
        for val in d.values():
            if isinstance(val, dict):
                score += calc_score(val)
            else:
                score += val
        d[sumkey] = score
        return score
    else:
        return d["_sum"]

calc_score(dirs)

# import json
# print(json.dumps(dirs, indent=4))

# search
total_score = 0
threshold = 100000

total_size = 70000000
required = 30000000
empty_size = total_size - dirs[sumkey]
needs = required - empty_size
best_size_found = total_size

stack = [dirs]
while stack:
    d = stack.pop()
    for val in d.values():
        if isinstance(val, dict):
            stack.append(val)
    s = d[sumkey]
    if s < threshold:
        total_score += s
    if s > needs and s < best_size_found:
        best_size_found = s
        
print(total_score)
print(best_size_found)
