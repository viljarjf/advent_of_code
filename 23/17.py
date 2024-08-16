import numpy as np


def main():
    
    with open("17_test", "r") as f:
        board = []
        for line in f:
            board.append([int(i) for i in line.strip()])
    board = np.array(board)
    
    graph = []

if __name__ == "__main__":
    main()
