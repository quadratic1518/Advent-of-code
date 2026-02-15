import sys


with open(sys.argv[1], "r") as f:
    data = f.read()

*gifts_s, trees_s = data.split("\n\n")

gifts = {}
for s in gifts_s:
    lines = s.split("\n")
    gifts[int(lines[0].strip(":"))] = lines[1:]

part1 = 0
for line in trees_s.split("\n"):
    dims_s, nums_s = line.split(": ")
    w, h = map(int, dims_s.split("x"))
    nums = list(map(int, nums_s.split(" ")))
    space = w * h
    min_space_needed = sum(c * "".join(gifts[i]).count("#") for i, c in enumerate(nums))
    if min_space_needed < space:
        part1 += 1

print(f"Part 1: {part1}")
