with open("04", "r") as f:
    board = [line.strip() for line in f]

# pad to avoid indexerror
empty = "." * len(board[0])
board = [empty] * 3 + board + [empty] * 3
for i, line in enumerate(board):
    board[i] = "..." + line + "..."

num_xmas = 0
for i, line in enumerate(board):
    for j, char in enumerate(line):
        # check the 8 different directions
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                num_xmas += (
                    board[i + 0*di][j + 0*dj] == "X" and 
                    board[i + 1*di][j + 1*dj] == "M" and 
                    board[i + 2*di][j + 2*dj] == "A" and 
                    board[i + 3*di][j + 3*dj] == "S"
                )


num_Xmas = 0
for i, line in enumerate(board):
    for j, char in enumerate(line):
        # check the 8 different directions
        num_Xmas += (
            board[i][j] == "A" and 
            {board[i - 1][j - 1], board[i + 1][j + 1]} == set("MS") and 
            {board[i + 1][j - 1], board[i - 1][j + 1]} == set("MS")
        )

print(num_xmas)
print(num_Xmas)
