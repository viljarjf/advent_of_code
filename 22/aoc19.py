## strategy: 
# give up
#
# start by figuring out if another machine should be produced, 
# to maximize production of a given resource. 
# I.e. do we want more ore machines if we want more clay in the end?

MAX_T = 24
N = 4
order = [
    "ore", 
    "clay",
    "obsidian",
    "geode"
]

blueprints = []
with open("input19.txt", "r") as f:
    for l in f:
        l = l.split()
        blueprints.append([
            [int(l[6]), 0, 0, 0],
            [int(l[12]), 0, 0, 0],
            [int(l[18]), int(l[21]), 0, 0],
            [int(l[27]), 0, int(l[30]), 0]
        ])

def calc_time_cost(
    robots: list[int], 
    inventory: list[int], 
    blueprint: list[list[int]]
    ) -> list[float]:
    time_costs = []
    for i in range(4):
        max_cost = -1
        for j in range(N):
            cost = max((blueprint[i][j] - inventory[j]), 0)
            r = robots[j]
            if cost == 0:
                r = 1
            elif r == 0:
                r = 1
                cost = float("inf")
            max_cost = max(max_cost, cost / r)
        time_costs.append(max_cost)
    return time_costs

for blueprint in blueprints:
    robots = [1, 0, 0, 0]
    inventory = [0, 0, 0, 0]

    t = 0
    while t < MAX_T:
        time_cost = calc_time_cost(robots, inventory, blueprint)
        for i in range(N):
            inventory[i] += robots[i]
        if time_cost[0] == 0:
            print(f"{t = }")
            robots[0] += 1
            for j in range(N):
                inventory[j] -= blueprint[0][j]
        t += 1
        
    print(inventory)
    
    

    

    
    
