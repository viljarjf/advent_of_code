import numpy as np
import numba

AIR = 0
ROCK = 1
BALL = 2

NORTH = 10
SOUTH = 11
EAST = 12
WEST = 13

NORTH_VECTOR = np.array([-1, 0])
SOUTH_VECTOR = np.array([1, 0])
EAST_VECTOR = np.array([0, 1])
WEST_VECTOR = np.array([0, -1])
VECTORS = {
    NORTH: NORTH_VECTOR,
    SOUTH: SOUTH_VECTOR,
    EAST: EAST_VECTOR,
    WEST: WEST_VECTOR,
}

@numba.njit
def move(board: np.ndarray, direction: int):
    # Oops, dicts and numba is a thing
    if direction == NORTH:
        dir_vec = NORTH_VECTOR
    elif direction == SOUTH:
        dir_vec = SOUTH_VECTOR
    elif direction == EAST:
        dir_vec = EAST_VECTOR
    else:
        dir_vec = WEST_VECTOR


    # find balls
    _inds = np.arange(board.size)[(board == BALL).flatten()]
    inds_x, inds_y = np.divmod(_inds, board.shape[1])
    inds = np.empty((inds_x.size, 2), dtype=np.int32)
    inds[:, 0] = inds_x
    inds[:, 1] = inds_y

    # move all balls untill none move
    keep_moving = True
    while keep_moving:
        keep_moving = False
        for i, ind in enumerate(inds):
            new_ind = ind + dir_vec
            if np.any(new_ind < 0) or new_ind[0] >= board.shape[0] or new_ind[1] >= board.shape[1]:
                continue 
            if board[new_ind[0], new_ind[1]] == AIR:
                board[ind[0], ind[1]] = AIR
                board[new_ind[0], new_ind[1]] = BALL
                inds[i] = new_ind
                keep_moving = True

def calc_load(board: np.ndarray) -> int:
    return np.sum((np.arange(board.shape[0]) + 1)[::-1] * np.sum(board == BALL, axis=1))

def cycle(board: np.ndarray):
    move(board, NORTH)
    move(board, WEST)
    move(board, SOUTH)
    move(board, EAST)

def calc_hash(board: np.ndarray) -> int:
    return calc_load(board) + 117*calc_load(board.T)

def main():
    boards: list[np.ndarray] = []
    with open("14", "r", encoding="utf-8") as inp:
        board = []
        for line in inp:
            if line.strip():
                line = line.strip().replace(".", str(AIR)).replace("O", str(BALL)).replace("#", str(ROCK))
                board.append([int(i) for i in line])
            else:
                boards.append(np.array(board))
                board = []
        # Add the last board
        boards.append(np.array(board))
        board = []

    # Whoops, there is only one board
    board = boards[0]
    board_1 = board.copy()
    move(board_1, NORTH)
    print(calc_load(board_1))

    hashes = []
    total_cycles = 1_000_000_000
    current_cycle = 0
    while current_cycle < total_cycles:
        current_cycle += 1
        print(f"{current_cycle = }")
        cycle(board)
        hash = calc_hash(board)
        if hash in hashes:
            # found a loop
            loop_length = hashes[::-1].index(hash) + 1
            remaining_loops = (total_cycles - current_cycle) // loop_length
            current_cycle += remaining_loops * loop_length
        else:
            hashes.append(hash)

    # move(board, NORTH)
    print(calc_load(board))


if __name__ == "__main__":
    main()
