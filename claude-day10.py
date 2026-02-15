import sys
import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

with open(sys.argv[1], "r") as f:
    data = f.read().strip()

def parse_line(line):
    lights_match = re.search(r'\[([.#]+)\]', line)
    lights = lights_match.group(1) if lights_match else ""

    buttons = re.findall(r'\(([0-9,]+)\)', line)
    buttons = [list(map(int, b.split(','))) for b in buttons]

    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = list(map(int, joltage_match.group(1).split(','))) if joltage_match else []

    return lights, buttons, joltage

def solve_part1_machine(lights, buttons):
    target = [1 if c == '#' else 0 for c in lights]
    n_lights = len(lights)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(t == 0 for t in target) else float('inf')

    # Build matrix in GF(2)
    matrix = []
    for i in range(n_lights):
        row = []
        for j in range(n_buttons):
            row.append(1 if i in buttons[j] else 0)
        row.append(target[i])
        matrix.append(row)

    # Gaussian elimination in GF(2)
    matrix = [row[:] for row in matrix]
    n_rows = len(matrix)
    n_cols = n_buttons

    pivot_cols = []
    row_idx = 0
    for col in range(n_cols):
        pivot = None
        for r in range(row_idx, n_rows):
            if matrix[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue

        matrix[row_idx], matrix[pivot] = matrix[pivot], matrix[row_idx]
        pivot_cols.append(col)

        for r in range(n_rows):
            if r != row_idx and matrix[r][col] == 1:
                for c in range(n_cols + 1):
                    matrix[r][c] ^= matrix[row_idx][c]

        row_idx += 1

    for r in range(row_idx, n_rows):
        if matrix[r][n_cols] == 1:
            return float('inf')

    n_pivots = len(pivot_cols)
    free_cols = [c for c in range(n_cols) if c not in pivot_cols]
    n_free = len(free_cols)

    min_presses = float('inf')

    for mask in range(1 << n_free):
        presses = [0] * n_cols

        for i, col in enumerate(free_cols):
            presses[col] = (mask >> i) & 1

        for i in range(n_pivots - 1, -1, -1):
            pivot_col = pivot_cols[i]
            val = matrix[i][n_cols]
            for c in range(n_cols):
                if c != pivot_col and matrix[i][c] == 1:
                    val ^= presses[c]
            presses[pivot_col] = val

        total = sum(presses)
        min_presses = min(min_presses, total)

    return min_presses

def solve_part2_machine(buttons, joltage):
    n_buttons = len(buttons)
    n_counters = len(joltage)

    if n_buttons == 0:
        return 0 if all(j == 0 for j in joltage) else float('inf')

    # Build A matrix: A[j][i] = 1 if button i affects counter j
    A = np.zeros((n_counters, n_buttons))
    for i, btn in enumerate(buttons):
        for j in btn:
            if j < n_counters:
                A[j][i] = 1

    b = np.array(joltage, dtype=float)

    # Objective: minimize sum of x_i
    c = np.ones(n_buttons)

    # Constraints: A @ x == b (equality)
    constraints = LinearConstraint(A, b, b)

    # Bounds: x_i >= 0
    bounds = Bounds(lb=0, ub=np.inf)

    # All variables are integers
    integrality = np.ones(n_buttons)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        return float('inf')

part1 = 0
part2 = 0

for line in data.split('\n'):
    if not line.strip():
        continue
    lights, buttons, joltage = parse_line(line)

    p1 = solve_part1_machine(lights, buttons)
    part1 += p1

    p2 = solve_part2_machine(buttons, joltage)
    part2 += p2

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
