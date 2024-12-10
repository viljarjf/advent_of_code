import numpy as np

CLEAR = 0
OBSTACLE = 1
GUARD = 3
KEYS = ".#^"

UP = 1
DOWN = 2
LEFT = 4
RIGHT = 8
DIRS = {
    (-1, 0): UP,
    (1, 0): DOWN,
    (0, -1): LEFT,
    (0, 1): RIGHT
}

def get_board(test: bool = True) -> np.ndarray:
    with open("06" + ("_test" if test else ""), "r") as f:
        lines = [line.strip() for line in f]
    lines = [[KEYS.index(c) for c in line] for line in lines]
    return np.array(lines)


def move(
    board: np.ndarray, 
    visited: np.ndarray,
    pos: tuple[int, int], 
    direction: tuple[int, int]
) -> tuple[
    np.ndarray, 
    np.ndarray, 
    tuple[int, int], 
    tuple[int, int], 
    bool
]:
    visited[pos] |= DIRS[direction]

    new_pos = tuple(sum(i) for i in zip(pos, direction))

    # bounds check
    if not 0 <= new_pos[0] < board.shape[0] or not 0 <= new_pos[1] < board.shape[1]:
        return board, visited, new_pos, direction, True

    if board[new_pos] == OBSTACLE:
        a, b = direction
        direction = (b, -a)
        return move(board, visited, pos, direction)
    return board, visited, new_pos, direction, False


def check_for_loop(
    board: np.ndarray, visited: np.ndarray, pos: tuple[int, int], direction: tuple[int, int]
) -> bool:
    while True:
        board, visited, pos, direction, oob = move(board, visited, pos, direction)
        if oob:
            return False
        if int(visited[pos]) & DIRS[direction]:
            # img = (visited != 0) + (board * 2)
            # img[pos] += 5
            # from matplotlib import pyplot as plt
            # plt.figure()
            # plt.imshow(img)
            # plt.show()
            return True


def run():
    board = get_board(False)
    visited = np.zeros_like(board)
    pos = init_pos = np.unravel_index(np.argmax(board), board.shape)
    direction = init_direction = (-1, 0)
    while True:
        
        board, visited, pos, direction, oob = move(board, visited, pos, direction)
        if oob:
            break
    print(np.count_nonzero(visited))

    # Uugh brute-forcing is no fun
    loops = 0
    visited[init_pos] = 0
    visited[init_pos[0] - 1, init_pos[1]] = 0
    while np.count_nonzero(visited):
        obstacle_pos = np.unravel_index(np.argmax(visited != 0), board.shape)
        visited[obstacle_pos] = 0
        obstacle_board = board.copy()
        obstacle_board[obstacle_pos] = OBSTACLE

        if check_for_loop(obstacle_board, np.zeros_like(visited), init_pos, init_direction):
            loops += 1
    
    print(loops) # 990 < ans < 2094

if __name__ == "__main__":
    run()
