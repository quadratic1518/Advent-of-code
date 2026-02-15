import sys
from collections import defaultdict


def count_neighbors(grid: defaultdict, r: int, c: int) -> int:
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if grid[(r + dr, c + dc)] and (dr != 0 or dc != 0):
                count += 1
    return count


def count_grid(grid: defaultdict) -> int:
    return sum(1 for r, c in list(grid) if grid[(r, c)])


with open(sys.argv[1], "r") as f:
    lines = list(map(str.strip, f.readlines()))


grid = defaultdict(bool)
for r, line in enumerate(lines):
    for c, ch in enumerate(line):
        grid[(r, c)] = ch == "@"

# for r in range(len(lines)):
#     for c in range(len(lines[0])):
#         if grid[(r,c)] == False:
#             out = ' '
#         elif count_neighbors(r, c) < 4:
#             out = 'x'
#         else:
#             out = '@'
#         print(out, end='')
#     print()
part1 = sum(1 for r, c in list(grid) if grid[(r, c)] and count_neighbors(grid, r, c) < 4)
print(f"Part 1: {part1}")

part2 = 0

while True:
    next_grid = defaultdict(bool)
    for r, c in list(grid):
        if grid[(r, c)] and count_neighbors(grid, r, c) >= 4:
            next_grid[(r, c)] = True
    diff = count_grid(grid) - count_grid(next_grid)
    if diff == 0:
        break
    part2 += diff
    grid = next_grid
print(f"Part 2: {part2}")
