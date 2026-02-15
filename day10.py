# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "z3-solver",
# ]
# ///
import sys
from itertools import combinations
from z3 import Optimize, Int, Sum, sat


def find_min_pushes(target, buttons):
    for i in range(1, len(buttons) + 1):
        for comb in combinations(buttons, i):
            result = 0
            for c in comb:
                result ^= c
            if result == target:
                return i


def find_min_pushes2(targets, buttons):
    opt = Optimize()
    x = [Int(f"x{i}") for i in range(len(buttons))]
    for xi in x:
        opt.add(xi >= 0)

    for i, target in enumerate(targets):
        coef = [int(i in button) for button in buttons]
        opt.add(Sum(xi * c for c, xi in zip(coef, x)) == target)

    opt.minimize(Sum(x))

    if opt.check() == sat:
        m = opt.model()
        return sum(m[xi].as_long() for xi in x)


with open(sys.argv[1], "r") as f:
    lines = list(map(str.strip, f.readlines()))

part1 = 0
part2 = 0
for line in lines:
    target_s, *buttons_s, power_s = line.split()
    target = int(target_s.strip("[]")[::-1].replace("#", "1").replace(".", "0"), 2)
    buttons = [
        sum(pow(2, int(b)) for b in button.strip("()").split(","))
        for button in buttons_s
    ]

    part1 += find_min_pushes(target, buttons)

    buttons2 = [list(map(int, b.strip("()").split(","))) for b in buttons_s]
    target2 = list(map(int, power_s.strip("{}").split(",")))
    part2 += find_min_pushes2(target2, buttons2)

print(f"Part 1: {part1}")

print(f"Part 2: {part2}")
