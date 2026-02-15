import math
import sys


with open(sys.argv[1], "r") as f:
    lines = f.readlines()

operators = lines[-1].split()
num_rows = [list(map(int, line.strip().split())) for line in lines[:-1]]

part1 = 0
for nums, op in zip(zip(*num_rows), operators):
    if op == "+":
        part1 += sum(nums)
    elif op == "*":
        part1 += math.prod(nums)
    else:
        raise

print(f"Part 1: {part1}")

part2 = 0
nums = []
op = ""
print()
for chars in zip(*lines):
    if all(c in " \n" for c in chars):
        if op == "+":
            part2 += sum(nums)
        elif op == "*":
            part2 += math.prod(nums)
        else:
            raise
        nums = []
        op = ""
        continue
    if chars[-1] in "*+":
        op = chars[-1]
    nums.append(int("".join(chars[:-1])))


print(f"Part 2: {part2}")
