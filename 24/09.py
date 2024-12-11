from itertools import chain

def get_inp(test: bool = True) -> str:
    with open("09_test" if test else "09", "r") as f:
        return f.read().strip()
    

def main():
    inp = get_inp(False)
    blocks = inp[::2]
    spaces = inp[1::2]
    
    # chain the same generators forwards and backwards, to exhaust them simultaneously
    def get_gen(num: int, reps: int):
        return (num for _ in range(reps))
    block_iter = []
    for i, b in enumerate(blocks):
        b = int(b)
        block_iter.append(get_gen(i, b))
    front = chain(*block_iter)
    back = chain(*block_iter[::-1])
    merged = []

    try:
        for block, space in zip(blocks, spaces):
            # Blocks
            size = int(block)
            for _ in range(size):
                merged.append(next(front))
            # Spaces
            size = int(space)
            for _ in range(size):
                merged.append(next(back))
    except StopIteration:
        pass
    s = sum(i * el for i, el in enumerate(merged))
    print(s)

    blocks_list = [[i] * int(el) for i, el in enumerate(blocks)]
    spaces_list = [[None] * int(el) for i, el in enumerate(spaces)]
    for block in blocks_list[::-1]:
        for space in spaces_list:
            if space.count(None) >= len(block):
                space[space.index(None):space.index(None) + len(block)] = block
                blocks_list[blocks_list.index(block)] = [None] * len(block)
                break
    merged = sum([a + b for a, b in zip(blocks_list, spaces_list)], start=[])
    s = sum(i * (0 if el is None else el) for i, el in enumerate(merged))
    print(s)

if __name__ == "__main__":
    main() # ans < 8612639490755
