import numpy as np
from dataclasses import dataclass
from collections import defaultdict
import heapq

@dataclass
class Tile:
    pos: tuple[int, int]
    dir: int
    val: int

    def __hash__(self) -> int:
        return hash((int(self.pos[0]), int(self.pos[1]), self.dir < RIGHT))
        return hash((int(self.pos[0]), int(self.pos[1]), self.dir))
    
    def __eq__(self, value: object) -> bool:
        return hash(value) == hash(self)
    
    def __lt__(self, other):
        return self.val < other.val

DOWN_VECTOR = np.array([1, 0])
UP_VECTOR = np.array([-1, 0])
RIGHT_VECTOR = np.array([0, 1])
LEFT_VECTOR = np.array([0, -1])
VECTORS = [DOWN_VECTOR, UP_VECTOR, RIGHT_VECTOR, LEFT_VECTOR]

DOWN    = 0
UP      = 1
RIGHT   = 2
LEFT    = 3

def insertsorted(tile: Tile, queue: list):
    # for i, old in enumerate(queue):
    #     if tile.val < old.val:
    #         queue.insert(i, tile)
    #         return
    heapq.heappush(queue, tile)

def explore(dir: int, tile: Tile, board: np.ndarray, queue: list, seen: defaultdict):
    pos = (tile.pos[0], tile.pos[1])
    total = tile.val
    for i in range(3):
        pos += VECTORS[dir]
        if (
            pos[0] < 0 or 
            pos[1] < 0 or 
            pos[0] >= board.shape[0] or 
            pos[1] >= board.shape[1]
        ):
            break
        total += board[tuple(pos)]
        tile = Tile((pos[0], pos[1]), dir, total)
        if seen[tile] > total:
            insertsorted(tile, queue)

def main():
    
    with open("17", "r") as f:
        board = []
        for line in f:
            board.append([int(i) for i in line.strip()])
    board = np.array(board)
    
    seen = defaultdict(lambda: 1 << 30)

    queue = [
        Tile((0, 0), RIGHT, 0),
        Tile((0, 0), DOWN, 0),
    ]
    pops = 0
    while queue:
        tile = heapq.heappop(queue)
        pos, dir_ind, total = tile.pos, tile.dir, tile.val
        if seen[tile] < int(total):
            continue
        seen[tile] = total
        pops += 1
        # Seperate check if we came from up/down or left/right
        if dir_ind in (UP, DOWN):
            explore(LEFT, tile, board, queue, seen)
            explore(RIGHT, tile, board, queue, seen)
        if dir_ind in (LEFT, RIGHT):
            explore(UP, tile, board, queue, seen)
            explore(DOWN, tile, board, queue, seen)
        if not pops % 100_000:
            
            print(f"{pops = }")
            print(f"{len(queue) = }")
            
    total = np.zeros_like(board)
    for idx in np.ndindex(board.shape):
        total[idx] = min([
            seen[Tile(idx, UP, 0)],
            seen[Tile(idx, DOWN, 0)],
            seen[Tile(idx, LEFT, 0)],
            seen[Tile(idx, RIGHT, 0)],
            ])
    print(f"{pops = }")
        
    import matplotlib
    matplotlib.use("QtAgg")

    from matplotlib import pyplot as plt
    plt.imshow(total)
    plt.show()
        



if __name__ == "__main__":
    main()
