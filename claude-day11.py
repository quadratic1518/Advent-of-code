import sys
from functools import cache

with open(sys.argv[1], "r") as f:
    data = f.read().strip()

# Parse graph: device -> list of outputs
graph = {}
for line in data.split('\n'):
    src, dests = line.split(': ')
    graph[src] = dests.split()

# Part 1: Count all paths from 'you' to 'out'
@cache
def count_paths(node):
    if node == 'out':
        return 1
    if node not in graph:
        return 0
    return sum(count_paths(n) for n in graph[node])

part1 = count_paths('you')
print(f"Part 1: {part1}")

# Part 2: Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'
# Use bitmask: 0=none, 1=dac, 2=fft, 3=both
@cache
def count_paths2(node, visited_mask):
    if node == 'dac':
        visited_mask |= 1
    if node == 'fft':
        visited_mask |= 2

    if node == 'out':
        return 1 if visited_mask == 3 else 0
    if node not in graph:
        return 0

    return sum(count_paths2(n, visited_mask) for n in graph[node])

part2 = count_paths2('svr', 0)
print(f"Part 2: {part2}")
