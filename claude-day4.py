import sys

with open(sys.argv[1], "r") as f:
    lines = f.read().strip().split("\n")

grid = [list(line) for line in lines]
rows = len(grid)
cols = len(grid[0])


def count_neighbors(grid, r, c):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == "@":
                    count += 1
    return count


def find_accessible(grid):
    accessible = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "@":
                if count_neighbors(grid, r, c) < 4:
                    accessible.append((r, c))
    return accessible


# Part 1: count initially accessible rolls
initial_accessible = find_accessible(grid)
part1 = len(initial_accessible)
print(f"Part 1: {part1}")

# Part 2: keep removing accessible rolls until none left
grid = [list(line) for line in lines]  # reset grid
total_removed = 0

while True:
    accessible = find_accessible(grid)
    if not accessible:
        break
    for r, c in accessible:
        grid[r][c] = "."
    total_removed += len(accessible)

print(f"Part 2: {total_removed}")
