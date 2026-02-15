import sys


with open(sys.argv[1], "r") as f:
    lines = list(map(str.strip, f.readlines()))

part1 = 0
part2 = 0
pos = 50

for line in lines:
    val = int(line.replace("L", "-").replace("R", ""))
    # pos = 0, L5
    if pos == 0 and val < 0:
        part2 -= 1
    pos = pos + val
    part2 += abs(pos // 100)
    # handles pos = 5, L5
    if pos == 0:
        part2 += 1
    # handles pos = 5, L105
    if pos % 100 == 0 and pos < 0:
        part2 += 1
    pos = pos % 100
    if pos == 0:
        part1 += 1

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
