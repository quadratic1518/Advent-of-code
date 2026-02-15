import sys

with open(sys.argv[1], "r") as f:
    grid = [list(line) for line in f.read().strip().split('\n')]

rows = len(grid)
cols = len(grid[0])

# Find starting position S
start_col = None
for c in range(cols):
    if grid[0][c] == 'S':
        start_col = c
        break

# Part 1: Count total splits
# Beams merge when they reach the same position
# Track which columns have beams (set), count splits when beam hits ^
beam_cols = {start_col}
total_splits = 0

for row in range(1, rows):
    new_beam_cols = set()
    for col in beam_cols:
        if grid[row][col] == '^':
            # Splitter: beam splits left and right
            total_splits += 1
            if col - 1 >= 0:
                new_beam_cols.add(col - 1)
            if col + 1 < cols:
                new_beam_cols.add(col + 1)
        else:
            # Empty space: beam continues down
            new_beam_cols.add(col)
    beam_cols = new_beam_cols

print(f"Part 1: {total_splits}")

# Part 2: Count distinct timelines (each path through is a timeline)
# A timeline is defined by the sequence of left/right choices at each splitter
# We track: column -> number of distinct timelines reaching that column
timelines = {start_col: 1}

for row in range(1, rows):
    new_timelines = {}
    for col, count in timelines.items():
        if grid[row][col] == '^':
            # Splitter: each timeline branches into two
            if col - 1 >= 0:
                new_timelines[col - 1] = new_timelines.get(col - 1, 0) + count
            if col + 1 < cols:
                new_timelines[col + 1] = new_timelines.get(col + 1, 0) + count
        else:
            # Empty space: timelines continue unchanged
            new_timelines[col] = new_timelines.get(col, 0) + count
    timelines = new_timelines

print(f"Part 2: {sum(timelines.values())}")
