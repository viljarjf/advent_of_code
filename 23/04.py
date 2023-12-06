matches = []
with open("04", "r", encoding="utf-8") as inp:
    for game in inp:
        winners, yours = game.split(":")[1].split("|")
        winners = [int(n) for n in winners.strip().split(" ") if n != ""]
        yours = [int(n) for n in yours.strip().split(" ") if n != ""]
        match_count = 0
        for n in yours:
            if n in winners:
                match_count += 1
        matches.append(match_count)
scores = [
    2 ** (n - 1)
    if n > 0
    else 0
    for n in matches
]
print(sum(scores))

import numpy as np
counts = np.ones_like(scores)
for i, (count, n) in enumerate(zip(counts, matches)):
    counts[i + 1 : i + 1 + n] += count

print(np.sum(counts))
