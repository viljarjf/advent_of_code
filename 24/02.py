def analyze(levels: list[int]) -> bool:
    diff = [a - b for a, b in zip(levels[:-1], levels[1:])]
    delta = [abs(d) <= 3 for d in diff]
    positive = [d > 0 for d in diff]
    negative = [d < 0 for d in diff]
    
    return all(delta) and (all(positive) or all(negative))

with open("02", "r") as f:
    safe = 0
    tolerated = 0
    for line in f:
        levels = [int(i) for i in line.strip().split()]
        
        safe_line = analyze(levels)
        safe += safe_line
        tolerated += safe_line
        if safe_line:
            continue
        
        for i in range(len(levels)):
            new = [l for l in levels] # copy
            new.pop(i)
            if analyze(new):
                tolerated += 1
                break
    print(safe)
    print(tolerated)
