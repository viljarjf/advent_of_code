# idea: shortest weighted path of length 30, weight = 1 / (distance * rate)

# Dont think that takes into account the time it takes to actually open the valve.
# Need to add another path of length 1 between each node then, 
# and instead find the longest path.
# But how do I then implement the 30 minute timeframe?

# Testing all combinations of visiting 30 nodes is too heavy..
# maybe do something greedy?

# What if we start out by finding the distance to all nodes first, 
# multiply the flow rate with the remaining time, and just continue from there?
# I dont think this has the correct properties..

# actually, maybe it would? lets do it and check

# Or maybe not. There are not too many valves.. what if we do greedy like 2 levels?
# Its "only" n^2. The main problem in this task is to find an algorithm that finds the solution,
# not finding an efficient algorithm, I think.

# shit, I just realised its not a directed graph.. maybe that will do something.
# Aight ill make a lookup table for shortest path between all nodes. 
# That's just BFS

# OOOH I think I got it maybe!
# Define a step as a walk + open. That has a certain flow rate, and takes a certain time.
# Make that the weight of that edge. 
# From the starting node, explore all options. 
# Distances from all nodes to all other nodes is easy to calculate, 
# so making each step is easy.
# Might need to do some pruning to reduce computation.
# Anyway, the weights will all become 0 after a couple steps! 
# We just need to find the longest path then!
# Hm, we must also consider that an opened valve cannot be opened again...
# I'll start with a greedy approach and take it from there

# Greedy gave the wrong answer...
# I'll have to iterate maybe

# maybe I can reduce this problem to a maximum flow with Ford-Fulkerson?
# Hm, might be difficult to remember which nodes have been explored..

# what if we begin from the other end?
# given n seconds, from any node, what is the best course of action?
# That should be greedy, I think

# Ended up basically hard-coding it. Took like 6s to run

# For task 2, I need each operator to go to the best available option, 
# where availability is affected by the other person too.
# Don't think that is quite as easy to implement as to describe...

# They are desynchronised... goddamn

# Maybe I need to rethink it a little. 
# What if I find the best course of action at each timestep, 
# instead of simplifying travel down to a target and a time

# I could just simulate each timestep, 
# and make each actor choose a decision from the tree constructed for solving task 1

# ...no, I don't think that would work. I'm stuck

# I think I'm content with solving only part 1

from dataclasses import dataclass
import numpy as np

T_MAX = 30
T_OPEN = 1
T_MOVE = 1

@dataclass
class Valve:
    name: str
    edges: list[str]
    flowrate: int
    
valves: dict[str, Valve] = dict()
indices = []
flows = []

with open("input16.txt", "r") as f:
    for l in f:
        l = l.replace(",","").split()
        v = l[1]
        r = int(l[4][5:-1])
        e = l[9:]
        valves[v] = Valve(v, e, r)
        indices.append(v)
        flows.append(r)

flows = np.array(flows)

distances = np.zeros((len(valves), len(valves)), dtype=np.int32) - 1

for i, valve in enumerate(indices):
    distances[i, i] = 0

    q = [(valve, T_MOVE + T_OPEN)]
    while q:
        v, d = q.pop(0) # queue => BFS
        # explore from valve v
        for _v in valves[v].edges:
            j = indices.index(_v)
            if distances[i, j] == -1:
                distances[i, j] = d
                q.append((_v, d + T_MOVE))


# current node, non-visited nodes, current flow, current time
i = indices.index("AA")
q = [(i, [j for j in range(len(indices)) if j != i], 0, T_MAX)]
max_flow = 0
while q:
    i, visits, flow, t = q.pop()
    max_flow = max(max_flow, flow)
    for j in visits:
        _t = t - distances[i, j]
        f = _t * flows[j]
        if f > 0:
            q.append((j, [l for l in visits if l != j], flow + f, _t))

print(max_flow)
