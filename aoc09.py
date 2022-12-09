with open("input90.txt", "r") as f:
    data = [i for i in f]

def move(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    sgn = lambda n: n // abs(n)
    x, y = tail
    if abs(dx) > 1:
        x += + sgn(dx)
        if abs(dy):
            y += sgn(dy)
    elif abs(dy) > 1:
        y +=sgn(dy)
        if abs(dx):
            x += sgn(dx)  
    return (x, y)

visited = set()
snakelen = 10
# head must be mutable, to move it easily.
# The rest must be immutable (since the tail is going in a set)
snake = [[0, 0]] + [(0,0) for _ in range(snakelen - 1)]

for step in data:
    d, l = step.split()
    headpos = snake[0]
    for _ in range(int(l)):
        if d == "R":
            headpos[0] += 1
        elif d == "L":
            headpos[0] -= 1
        elif d == "U":
            headpos[1] += 1
        elif d == "D":
            headpos[1] -= 1
        for i in range(1, snakelen):
            snake[i] = move(snake[i-1], snake[i])
        visited.add(snake[-1])

print(len(visited))
