import sys

with open(sys.argv[1], "r") as f:
    lines = f.read().strip().split("\n")

def max_joltage(bank, k):
    # Greedy: at each position, decide whether to include this digit
    # We need exactly k digits total, so we have constraints on how many we can skip
    n = len(bank)
    result = []
    i = 0
    for _ in range(k):
        # We need to pick (k - len(result)) more digits from remaining positions
        remaining_needed = k - len(result)
        # Latest position we can pick from: n - remaining_needed
        max_pos = n - remaining_needed
        # Find the largest digit in range [i, max_pos]
        best_digit = '0'
        best_idx = i
        for j in range(i, max_pos + 1):
            if bank[j] > best_digit:
                best_digit = bank[j]
                best_idx = j
        result.append(best_digit)
        i = best_idx + 1
    return int("".join(result))

# Part 1: pick exactly 2 batteries from each bank
part1 = sum(max_joltage(line, 2) for line in lines)
print(f"Part 1: {part1}")

# Part 2: pick exactly 12 batteries from each bank
part2 = sum(max_joltage(line, 12) for line in lines)
print(f"Part 2: {part2}")
