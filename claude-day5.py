import sys

with open(sys.argv[1], "r") as f:
    data = f.read().strip()

parts = data.split("\n\n")
ranges_raw = parts[0].split("\n")
ranges = []
for line in ranges_raw:
    start, end = map(int, line.split("-"))
    ranges.append((start, end))

# Part 1: count available ingredient IDs that are fresh
if len(parts) > 1:
    ingredients = list(map(int, parts[1].split("\n")))
    part1 = 0
    for ing in ingredients:
        for start, end in ranges:
            if start <= ing <= end:
                part1 += 1
                break
    print(f"Part 1: {part1}")

# Part 2: count total unique IDs covered by all ranges (merge overlapping)
# Sort ranges by start, then merge overlapping
ranges.sort()
merged = []
for start, end in ranges:
    if merged and start <= merged[-1][1] + 1:
        merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    else:
        merged.append((start, end))

part2 = sum(end - start + 1 for start, end in merged)
print(merged)
print(f"Part 2: {part2}")
