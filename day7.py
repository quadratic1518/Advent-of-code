import sys
from collections import defaultdict

with open(sys.argv[1], "r") as f:
    lines = list(map(str.strip, f.readlines()))

# beams = [lines[0].index('S')]
beams = {lines[0].index("S"): 1}
part1 = 0

for line in lines[1:]:
    next_beams = defaultdict(int)
    for beam in beams:
        if line[beam] == ".":
            next_beams[beam] += beams[beam]
        elif line[beam] == "^":
            next_beams[beam - 1] += beams[beam]
            next_beams[beam + 1] += beams[beam]
            part1 += 1
    beams = next_beams

print(f"Part 1: {part1}")

part2 = sum(beams.values())
print(f"Part 2: {part2}")
