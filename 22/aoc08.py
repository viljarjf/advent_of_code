import numpy as np

# instead of counting from the edge, I'll just find out which trees are visible

with open("input08.txt", "r") as f:
    data = np.pad([[int(j) for j in i.strip()] for i in f], (1, 1), "constant", constant_values=-1)

visible1 = 0*data.copy() # look up
visible2 = 0*data.copy() # look left
visible3 = 0*data.copy() # look down
visible4 = 0*data.copy() # look right

visibility1 = 0*data.copy() # look up
visibility2 = 0*data.copy() # look left
visibility3 = 0*data.copy() # look down
visibility4 = 0*data.copy() # look right

im = data.shape[0]
jm = data.shape[1]
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        d = data[i, j]

        for n in range(i-1, -1, -1):
            visibility1[i, j] += 1
            if d <= data[n, j]:
                visible1[i, j] = 0
                break
            # this would make the code faster (memoizing) but introduces duplicate code
            # elif visible1[n, j]:
            #     visible1[i, j] = 1
            #     break
        else:
            visible1[i, j] = 1
               
        for n in range(j-1, -1, -1):
            visibility2[i, j] += 1
            if d <= data[i, n]:
                visible2[i, j] = 0
                break
        else:
            visible2[i, j] = 1

        for n in range(i+1, im):
            visibility3[i, j] += 1
            if d <= data[n, j]:
                visible3[i, j] = 0
                break
        else:
            visible3[i, j] = 1

        for n in range(j+1, jm):
            visibility4[i, j] += 1
            if d <= data[i, n]:
                visible4[i, j] = 0
                break
        else:
            visible4[i, j] = 1

visible1 = visible1[1:-1, 1:-1]
visible2 = visible2[1:-1, 1:-1]
visible3 = visible3[1:-1, 1:-1]
visible4 = visible4[1:-1, 1:-1]
visibility1 = visibility1[1:-1, 1:-1] - visible1
visibility2 = visibility2[1:-1, 1:-1] - visible2
visibility3 = visibility3[1:-1, 1:-1] - visible3
visibility4 = visibility4[1:-1, 1:-1] - visible4

visible = visible1 | visible2 | visible3 | visible4
print(np.count_nonzero(visible))

view = visibility1 * visibility2 * visibility3 * visibility4
print(view.max())
