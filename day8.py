import sys
from collections import defaultdict
from math import prod


with open(sys.argv[1], "r") as f:
    lines = list(map(str.strip, f.readlines()))

points = []
for line in lines:
    x, y, z = map(int, line.split(","))
    points.append((x, y, z))

dists = []
for n, (x1, y1, z1) in enumerate(points):
    for m, (x2, y2, z2) in enumerate(points):
        if n < m:
            dist = pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2)
            dists.append((dist, n, m))

parent = {i: i for i in range(len(points))}


def find_set(v):
    if v == parent[v]:
        return v
    parent[v] = find_set(parent[v])
    return parent[v]


def merge_sets(a, b):
    parent[find_set(b)] = find_set(a)


wire_count = 10 if len(points) < 100 else 1000
connections = 0
for i, (d, n, m) in enumerate(sorted(dists)):
    if i == wire_count:
        sizes = defaultdict(int)
        for x in range(len(points)):
            sizes[find_set(x)] += 1
        part1 = prod(sorted(sizes.values(), reverse=True)[:3])
        print(f"Part 1: {part1}")

    n_rep = find_set(n)
    m_rep = find_set(m)
    if n_rep != m_rep:
        connections += 1
        merge_sets(n, m)
        if connections == len(points) - 1:
            part2 = points[n][0] * points[m][0]
            print(f"Part 2: {part2}")
            break
