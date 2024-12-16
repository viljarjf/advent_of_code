import numpy as np

EMPTY = 0
WALL = 1
BOX = 2
ROBOT = 3
BOX_LEFT = 4
BOX_RIGHT = 5

def parse_input(testing: bool = False) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # with open("15_test" if testing else "15", "r") as f:
    with open("24/15_test" if testing else "24/15", "r") as f:
        map = []
        large_map = []
        instructions = []
        
        directions = {
            "<": (0, -1),
            ">": (0, 1),
            "^": (-1, 0),
            "v": (1, 0)
        }
        objects = {
            "#": WALL,
            "@": ROBOT,
            "O": BOX,
            ".": EMPTY,
            "[": BOX_LEFT,
            "]": BOX_RIGHT,
        }
        large_objects = {
            "#": "##",
            ".": "..",
            "O": "[]",
            "@": "@.",
        }

        for line in f:
            if not line.strip():
                break
            map.append([objects[c] for c in line.strip()])
            # As I understand it, writing unmaintainable code is a great way to 
            # both increase job security and the likelyhood of being fired
            large_map.append(list(sum(zip(
                [objects[large_objects[c][0]] for c in line.strip()],
                [objects[large_objects[c][1]] for c in line.strip()],
            ), ())))
        for line in f:
            instructions += [directions[c] for c in line.strip()]
    return np.array(map), np.array(large_map), np.array(instructions)


def can_move(map: np.ndarray, pos: tuple[int, int], direction: tuple[int, int]) -> bool:
    new_pos = (
        pos[0] + direction[0],
        pos[1] + direction[1],
    )
    if map[new_pos] == WALL:
        return False
    out = False
    if map[new_pos] == EMPTY:
        out = True
    elif can_move(map, new_pos, direction):
        out = True

    if map[pos] == BOX_LEFT:
        right = (pos[0], pos[1] + 1)
        map[right] = BOX
        out &= can_move(map, right, direction)
        map[right] = BOX_RIGHT
    elif map[pos] == BOX_RIGHT:
        left = (pos[0], pos[1] - 1)
        map[left] = BOX
        out &= can_move(map, left, direction)
        map[left] = BOX_LEFT
    
    return out

def move(map: np.ndarray, pos: tuple[int, int], direction: tuple[int, int]) -> bool:
    if not can_move(map, pos, direction):
        return False
    new_pos = (
        pos[0] + direction[0],
        pos[1] + direction[1],
    )
    if map[new_pos] != EMPTY:
        move(map, new_pos, direction)
    if map[pos] == BOX_LEFT:
        right = (pos[0], pos[1] + 1)
        map[right] = BOX
        move(map, right, direction)
        map[right[0] + direction[0], right[1] + direction[1]] = BOX_RIGHT
    if map[pos] == BOX_RIGHT:
        left = (pos[0], pos[1] - 1)
        map[left] = BOX
        move(map, left, direction)
        map[left[0] + direction[0], left[1] + direction[1]] = BOX_LEFT
    map[new_pos] = map[pos]
    map[pos] = EMPTY
    return True

def calculate_score(map: np.ndarray) -> int:
    boxes = np.argwhere(map == BOX)
    boxes[:, 0] *= 100
    return boxes.sum()

def main():
    map, large_map, instructions = parse_input()
    for direction in instructions:
        pos = np.nonzero(map == ROBOT)
        move(map, pos, direction)
        pos = np.nonzero(large_map == ROBOT)
        move(large_map, pos, direction)
    print(calculate_score(map))

if __name__ == "__main__":
    main()
