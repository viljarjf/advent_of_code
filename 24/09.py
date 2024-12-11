from itertools import chain
from dataclasses import dataclass

@dataclass
class Node:
    size: int
    ind: int = None
    prev: "Node" = None
    next: "Node" = None
    def __repr__(self):
        if self.ind is None:
            return f"Space({self.size})"
        return f"Node({self.size}, {self.ind})"
    
def print_blocks(start: Node):
    assert start.prev is None
    out = ""
    node = start
    while node is not None:
        out += ("." if node.ind is None else str(node.ind)) * node.size
        node = node.next
    print(out)

def sum_blocks(start: Node) -> int:
    assert start.prev is None
    out = []
    node = start
    while node is not None:
        out += [0 if node.ind is None else node.ind] * node.size
        node = node.next
    return sum(i * el for i, el in enumerate(out))

def get_inp(test: bool = True) -> str:
    file = __file__[:-3]
    with open(f"{file}_test" if test else file, "r") as f:
        return f.read().strip()
    
def part_1():
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

def main():
    part_1()

    inp = get_inp(False)
    blocks = inp[::2]
    spaces = inp[1::2]

    # Make linked list
    a = [Node(int(el), i) for i, el in enumerate(blocks)]
    b = [Node(int(el)) for el in spaces]
    full: list[Node] = list(chain(*zip(a, b))) + [a[-1]]
    # Create links
    for a, b in zip(full[:-1], full[1:]):
        a.next = b
        b.prev = a
    start = full[0]
    cur = start
    for node in full[::-1]:
        if node.ind is None:
            continue
        cur = start
        # Find suitable space
        while cur.next is not None:
            if cur.ind is None and cur.size >= node.size or cur is node:
                break
            cur = cur.next
        else:
            print("Found no space for", node)
            continue
        if cur is node:
            continue
        # Ugh linked lists was not fun
        
        # insert space where the node was
        old_left = node.prev
        old_right = node.next
        new_space = Node(node.size, None, old_left, old_right)
        old_left.next = new_space 
        if old_right is not None:
            old_right.prev = new_space
        
        left = cur.prev
        left.next = node
        node.prev = left

        right = cur.next
        cur.size -= node.size
        if cur.size > 0:
            node.next = cur
            cur.prev = node
            cur.next = right
            right.prev = cur
        else:
            node.next = right
            right.prev = node
            del cur
    print_blocks(start)
    print(sum_blocks(start))
    
if __name__ == "__main__":
    main()
