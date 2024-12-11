# lmao lets do regex

import re

test = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
with open("03", "r") as f:
    real = f.read()

f = r"mul\(([1-9]|[1-9][0-9]|[1-9][0-9][0-9]),([1-9]|[1-9][0-9]|[1-9][0-9][0-9])\)"

res = re.findall(f, real)
print(sum(int(a)*int(b) for a, b in res))

do = re.split(f"do\(\)", real)
do = "".join(re.split(f"don't\(\)", s)[0] for s in do)
res = re.findall(f, do)
print(sum(int(a)*int(b) for a, b in res))

