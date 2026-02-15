import sys
import re


def is_invalid(i: int) -> bool:
    code = str(i)
    if len(code) % 2 != 0:
        return False
    return code[: len(code) // 2] == code[len(code) // 2 :]


def is_invalid_regex(i: int) -> bool:
    return bool(re.fullmatch(r"(.+)\1", str(i)))


# precompiling regex takes part 2 down from 1.34
# seconds to 0.86
part2_regex = re.compile(r"(.+)\1+")


def is_invalid_regex_part2(i: int) -> bool:
    # return bool(re.fullmatch(r"(.+)\1+", str(i)))
    return bool(part2_regex.fullmatch(str(i)))


with open(sys.argv[1], "r") as f:
    ranges = f.read().strip().split(",")

part1 = 0
part2 = 0
for r in ranges:
    start, end = map(int, r.split("-"))
    for i in range(start, end + 1):
        # if is_invalid(i):
        #     part1 += i
        if is_invalid_regex_part2(i):
            part2 += i

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
