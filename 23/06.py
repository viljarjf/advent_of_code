import numpy as np

# Test
times = [7, 15, 30]
distances = [9, 40, 200]

# Real
times = [41, 77, 70, 96]
distances = [249, 1362, 1127, 1011]

number_of_ways_to_beat_the_record = []
for time, record in zip(times, distances):
    waiting_times = np.arange(0, time + 1)
    speeds = waiting_times.copy()
    travel_times = time - waiting_times
    possible_distances = speeds * travel_times
    number_of_ways_to_beat_the_record.append(np.count_nonzero(possible_distances > record))
print(np.prod(number_of_ways_to_beat_the_record))

time = int("".join(str(t) for t in times))
record = int("".join(str(d) for d in distances))

# only check first half for when the first win is.
# Count the remaining times in the first half, and double it.
# Could probably use some kind of binary search but whatever
for t in range(time // 2):
    speed = t
    travel_time = time - t
    distance = speed * travel_time
    if distance > record:
        print(time - 2*t + 1)
        break
