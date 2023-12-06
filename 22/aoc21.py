import sympy

m = dict()

with open("input21.txt", "r") as f:
    for l in f:
        key, val = l.split(":")
        val = val.strip()
        if " " not in val:
            m[key] = int(val)
        else:
            m[key] = val

old_humn = m["humn"]
humn = sympy.symbols("humn")
m["humn"] = humn
old_root = m["root"]

def get(key: str) -> sympy.Add: 
    if isinstance(m[key], str):
        a, op, b = m[key].split()
        if op == "+":
            m[key] = get(a) + get(b)
        elif op == "-":
            m[key] = get(a) - get(b)
        elif op == "*":
            m[key] = get(a) * get(b)
        elif op == "/":
            m[key] = get(a) / get(b)
    return m[key]

print(get("root").replace(humn, old_humn))
a, _, b = old_root.split()

print(sympy.solve(get(a) - get(b), humn))
