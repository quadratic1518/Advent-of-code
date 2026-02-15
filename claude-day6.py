import sys

with open(sys.argv[1], "r") as f:
    lines = f.read().rstrip('\n').split('\n')

# Part 1: Read left-to-right, numbers arranged vertically
# Find problems separated by blank columns
def parse_part1(lines):
    if not lines:
        return 0

    # Find the operator line (last non-empty line)
    op_line = lines[-1]
    num_lines = lines[:-1]

    # Find column groups (problems separated by space-only columns)
    width = max(len(line) for line in lines)
    # Pad all lines to same width
    padded = [line.ljust(width) for line in lines]

    # Find separator columns (all spaces in that column for num_lines)
    def is_separator(col):
        for line in padded[:-1]:  # exclude operator line
            if col < len(line) and line[col] != ' ':
                return False
        return True

    # Group columns into problems
    problems = []
    current_cols = []
    for col in range(width):
        if is_separator(col):
            if current_cols:
                problems.append(current_cols)
                current_cols = []
        else:
            current_cols.append(col)
    if current_cols:
        problems.append(current_cols)

    # For each problem, extract numbers and operator
    total = 0
    for cols in problems:
        # Get operator (from the operator line, find non-space char in these cols)
        op = None
        for c in cols:
            if c < len(op_line) and op_line[c] in '+*':
                op = op_line[c]
                break
        if op is None:
            continue

        # Extract numbers from each row
        numbers = []
        for line in num_lines:
            num_str = ''.join(line[c] if c < len(line) else ' ' for c in cols).strip()
            if num_str:
                numbers.append(int(num_str))

        # Calculate result
        if op == '+':
            result = sum(numbers)
        else:  # *
            result = 1
            for n in numbers:
                result *= n
        total += result

    return total

# Part 2: Read right-to-left in columns, digits vertically (most significant at top)
def parse_part2(lines):
    if not lines:
        return 0

    op_line = lines[-1]
    num_lines = lines[:-1]

    width = max(len(line) for line in lines)
    padded = [line.ljust(width) for line in lines]

    # Find separator columns
    def is_separator(col):
        for line in padded[:-1]:
            if col < len(line) and line[col] != ' ':
                return False
        return True

    # Group columns into problems (reading right to left now for processing)
    problems = []
    current_cols = []
    for col in range(width):
        if is_separator(col):
            if current_cols:
                problems.append(current_cols)
                current_cols = []
        else:
            current_cols.append(col)
    if current_cols:
        problems.append(current_cols)

    # For each problem, read columns right-to-left
    # Each column becomes a number, digits read top-to-bottom
    total = 0
    for cols in problems:
        op = None
        for c in cols:
            if c < len(op_line) and op_line[c] in '+*':
                op = op_line[c]
                break
        if op is None:
            continue

        # Read each column as a number (right-to-left through columns)
        numbers = []
        for c in reversed(cols):  # right to left
            digits = []
            for line in num_lines:
                char = line[c] if c < len(line) else ' '
                if char.isdigit():
                    digits.append(char)
            if digits:
                numbers.append(int(''.join(digits)))

        # Calculate result
        if op == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n
        total += result

    return total

part1 = parse_part1(lines)
print(f"Part 1: {part1}")

part2 = parse_part2(lines)
print(f"Part 2: {part2}")
