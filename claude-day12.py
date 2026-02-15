import sys

def parse_input(data):
    lines = data.strip().split('\n')
    shapes = {}
    regions = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue

        if 'x' in line and ':' in line:
            parts = line.split(':')
            dims = parts[0].strip()
            width, height = map(int, dims.split('x'))
            quantities = list(map(int, parts[1].strip().split()))
            regions.append((width, height, quantities))
            i += 1
        elif len(line) >= 1 and line.rstrip(':').isdigit():
            idx = int(line.rstrip(':'))
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i] and ':' not in lines[i]:
                shape_lines.append(lines[i])
                i += 1
            cells = set()
            for r, row in enumerate(shape_lines):
                for c, ch in enumerate(row):
                    if ch == '#':
                        cells.add((r, c))
            if cells:
                shapes[idx] = cells
        else:
            i += 1

    return shapes, regions

def get_all_orientations(shape):
    def normalize(cells):
        min_r = min(r for r, c in cells)
        min_c = min(c for r, c in cells)
        return frozenset((r - min_r, c - min_c) for r, c in cells)

    def rotate(cells):
        return set((c, -r) for r, c in cells)

    def flip_h(cells):
        return set((r, -c) for r, c in cells)

    current = set(shape)
    seen = set()
    orientations = []

    for _ in range(4):
        norm = normalize(current)
        if norm not in seen:
            seen.add(norm)
            orientations.append(norm)
        flipped = flip_h(current)
        norm_f = normalize(flipped)
        if norm_f not in seen:
            seen.add(norm_f)
            orientations.append(norm_f)
        current = rotate(current)

    return orientations

def solve_region(width, height, quantities, all_orientations, shape_sizes):
    # Quick area check
    area = width * height
    needed = sum(quantities[i] * shape_sizes[i] for i in range(len(quantities)))
    if needed > area:
        return False

    # Build list of shapes to place (sort by size descending for better pruning)
    shapes_to_place = []
    for shape_idx, qty in enumerate(quantities):
        for _ in range(qty):
            shapes_to_place.append(shape_idx)

    if not shapes_to_place:
        return True

    # Sort by shape size (larger first) for better pruning
    shapes_to_place.sort(key=lambda x: -shape_sizes[x])

    # Precompute all placements for each shape
    def get_placements_at(orientation, height, width):
        max_r = max(r for r, c in orientation)
        max_c = max(c for r, c in orientation)
        result = []
        for start_r in range(height - max_r):
            for start_c in range(width - max_c):
                result.append(frozenset((start_r + r, start_c + c) for r, c in orientation))
        return result

    shape_placements = {}
    for shape_idx in set(shapes_to_place):
        placements = []
        for orientation in all_orientations[shape_idx]:
            placements.extend(get_placements_at(orientation, height, width))
        shape_placements[shape_idx] = list(set(placements))

    # Use bit manipulation for faster set operations
    cell_to_bit = {}
    for r in range(height):
        for c in range(width):
            cell_to_bit[(r, c)] = 1 << (r * width + c)

    shape_placement_bits = {}
    for shape_idx, placements in shape_placements.items():
        bits = []
        for p in placements:
            b = 0
            for cell in p:
                b |= cell_to_bit[cell]
            bits.append(b)
        shape_placement_bits[shape_idx] = bits

    # Backtracking with bitmask
    def backtrack(idx, occupied):
        if idx == len(shapes_to_place):
            return True

        shape_idx = shapes_to_place[idx]
        for bits in shape_placement_bits[shape_idx]:
            if (occupied & bits) == 0:
                if backtrack(idx + 1, occupied | bits):
                    return True

        return False

    return backtrack(0, 0)

def main():
    with open(sys.argv[1], 'r') as f:
        data = f.read()

    shapes, regions = parse_input(data)

    all_orientations = {idx: get_all_orientations(cells) for idx, cells in shapes.items()}
    shape_sizes = {idx: len(cells) for idx, cells in shapes.items()}

    count = 0
    for i, (width, height, quantities) in enumerate(regions):
        if solve_region(width, height, quantities, all_orientations, shape_sizes):
            count += 1

    print(f"Part 1: {count}")

if __name__ == "__main__":
    main()
