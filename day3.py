import sys


def find_max_power(bank: list[int], count: int = 2) -> int:
    answer = 0
    for i in range(-count + 1 , 1):
        offset = i if i != 0 else None
        digit = max(bank[:offset])
        answer = (answer * 10) + digit
        bank = bank[bank.index(digit)+1:]
    return answer


with open(sys.argv[1], 'r') as f:
    lines = list(map(str.strip, f.readlines()))


part1 = 0
part2 = 0
for line in lines:
    nums = [int(c) for c in line]
    part1 += find_max_power(nums)
    part2 += find_max_power(nums, 12)
    # first = max(nums[:-1])
    # second = max(nums[nums.index(first)+1:])
    # part1 += int(f"{first}{second}")

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')