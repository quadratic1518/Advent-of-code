import sys
from math import sqrt

with open(sys.argv[1], "r") as f:
    data = f.read().strip()

# Parse junction boxes
boxes = []
for line in data.split('\n'):
    x, y, z = map(int, line.split(','))
    boxes.append((x, y, z))

n = len(boxes)

# Calculate all pairwise distances
distances = []
for i in range(n):
    for j in range(i + 1, n):
        x1, y1, z1 = boxes[i]
        x2, y2, z2 = boxes[j]
        dist = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        distances.append((dist, i, j))

# Sort by distance
distances.sort()

# Union-Find
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py:
        return False  # Already in same circuit
    if rank[px] < rank[py]:
        px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]:
        rank[px] += 1
    return True

# Part 1: Connect 1000 closest pairs and find 3 largest circuits
# (for the example, use 10 connections)
target_connections = 1000 if n > 100 else 10
connections = 0
for dist, i, j in distances:
    union(i, j)
    connections += 1
    if connections == target_connections:
        break

# Count circuit sizes
circuit_sizes = {}
for i in range(n):
    root = find(i)
    circuit_sizes[root] = circuit_sizes.get(root, 0) + 1

sizes = sorted(circuit_sizes.values(), reverse=True)
part1 = sizes[0] * sizes[1] * sizes[2]
print(f"Part 1: {part1}")

# Part 2: Reset and continue until all in one circuit, find last connection
parent = list(range(n))
rank = [0] * n

last_i, last_j = None, None
num_circuits = n

for dist, i, j in distances:
    if union(i, j):
        num_circuits -= 1
        last_i, last_j = i, j
        if num_circuits == 1:
            break

part2 = boxes[last_i][0] * boxes[last_j][0]
print(f"Part 2: {part2}")
