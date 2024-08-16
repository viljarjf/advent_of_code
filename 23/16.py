import numpy as np
from matplotlib import pyplot as plt

NORTH_VECTOR = np.array([1, 0])
SOUTH_VECTOR = np.array([-1, 0])
EAST_VECTOR = np.array([0, 1])
WEST_VECTOR = np.array([0, -1])
VECTORS = [NORTH_VECTOR, SOUTH_VECTOR, EAST_VECTOR, WEST_VECTOR]
# indices
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

MAP = {j: i for i, j in enumerate("./\\|-")}


def explore(board, queue):
    discovered = np.zeros_like(board)

    while queue:
        pos, dir = queue.pop(0)
        pos = tuple(pos)
        # bounds check
        if pos[0] < 0 or pos[0] >= board.shape[0] or pos[1] < 0 or pos[1] >= board.shape[1]:
            continue
        # Check if we have been here before
        heading = 1 << dir
        if int(discovered[pos]) & heading:
            continue
        discovered[pos] |= heading

        # Next tile(s)
        if board[pos] == MAP["."]:
            queue.append((pos + VECTORS[dir], dir))
        elif board[pos] == MAP["/"]:
            if dir == NORTH:
                queue.append((pos + WEST_VECTOR, WEST))
            elif dir == WEST:
                queue.append((pos + NORTH_VECTOR, NORTH))
            elif dir == SOUTH:
                queue.append((pos + EAST_VECTOR, EAST))
            elif dir == EAST:
                queue.append((pos + SOUTH_VECTOR, SOUTH))
        elif board[pos] == MAP["\\"]:
            if dir == NORTH:
                queue.append((pos + EAST_VECTOR, EAST))
            elif dir == EAST:
                queue.append((pos + NORTH_VECTOR, NORTH))
            elif dir == SOUTH:
                queue.append((pos + WEST_VECTOR, WEST))
            elif dir == WEST:
                queue.append((pos + SOUTH_VECTOR, SOUTH))
        elif board[pos] == MAP["|"]:
            if dir == NORTH or dir == SOUTH:
                queue.append((pos + VECTORS[dir], dir))
            else:
                queue.append((pos + NORTH_VECTOR, NORTH))
                queue.append((pos + SOUTH_VECTOR, SOUTH))
        elif board[pos] == MAP["-"]:
            if dir == EAST or dir == WEST:
                queue.append((pos + VECTORS[dir], dir))
            else:
                queue.append((pos + EAST_VECTOR, EAST))
                queue.append((pos + WEST_VECTOR, WEST))
    
    return discovered

def main():
    board = []
    with open("16", "r", encoding="utf-8") as inp:
        for line in inp:
            board.append([MAP[char] for char in line.strip()])
    
    board = np.array(board)
    init = [(
            (0, 0),
            EAST,
        )]
    print(np.count_nonzero(explore(board, init)))

    full = [((0, i), EAST) for i in range(board.shape[0])] + \
    [((board.shape[0], i), WEST) for i in range(board.shape[0])] + \
    [((i, 0), NORTH) for i in range(board.shape[1])] + \
    [((i, board.shape[1]), WEST) for i in range(board.shape[1])]

    boards = [explore(board.copy(), [i]) for i in full]
    print(max(np.count_nonzero(b) for b in boards))

if __name__ == "__main__":
    main()
