import sys


with open(sys.argv[1], "r") as f:
    raw_input = f.read()
raw_ranges, raw_ingreds = raw_input.split("\n\n")

ranges = []
for r in raw_ranges.splitlines():
    s, e = map(int, r.split("-"))
    ranges.append((s, e))

part1 = 0
for ingred_str in raw_ingreds.splitlines():
    ingred = int(ingred_str)
    fresh = 0
    for s, e in ranges:
        if s <= ingred <= e:
            fresh = 1
            break
    part1 += fresh

print(f"Part 1: {part1}")

part2 = 0
idx = 0
for s, e in sorted(ranges):
    if s <= idx:
        s = idx + 1
    if e >= s:
        part2 += e - s + 1
    idx = max(e, idx)

print(f"Part 2: {part2}")
