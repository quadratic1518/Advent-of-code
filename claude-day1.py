import sys

with open(sys.argv[1], "r") as f:
    lines = f.read().strip().split("\n")

pos = 50
part1 = 0
part2 = 0

for line in lines:
    direction = line[0]
    distance = int(line[1:])

    if direction == "L":
        # Count how many times we pass through 0 going left
        # Going left from pos by distance clicks
        for _ in range(distance):
            pos = (pos - 1) % 100
            if pos == 0:
                part2 += 1
    else:  # R
        # Going right from pos by distance clicks
        for _ in range(distance):
            pos = (pos + 1) % 100
            if pos == 0:
                part2 += 1

    if pos == 0:
        part1 += 1

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
