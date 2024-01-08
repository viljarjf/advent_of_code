from collections import OrderedDict

def hash(chars: str) -> int:
    out = 0
    for c in chars:
        out += ord(c)
        out *= 17
        out %= 256
    return out

def calc_score(boxes: list[OrderedDict]) -> int:
    score = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box.values()):
            score += (i + 1) * (j + 1) * lens
    return score

def main():
    boxes = [OrderedDict() for _ in range(256)]
    with open("15", "r") as inp:
        for thing in inp.readline().strip().split(","):
            if "-" in thing:
                key = thing[:-1]
                ind = hash(key)
                if key in boxes[ind]:
                    boxes[ind].pop(key)
            elif "=" in thing:
                key, lens = thing.split("=")
                ind = hash(key)
                boxes[ind][key] = int(lens)
        print(calc_score(boxes))

if __name__ == "__main__":
    main()
