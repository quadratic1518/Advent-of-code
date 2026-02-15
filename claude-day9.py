import sys

with open(sys.argv[1], "r") as f:
    data = f.read().strip()

# Parse coordinates
points = []
for line in data.split('\n'):
    x, y = map(int, line.split(','))
    points.append((x, y))

# Part 1: Find largest rectangle area using any two points as opposite corners
# Area includes both corner tiles, so it's (width+1) * (height+1)
max_area = 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        x1, y1 = points[i]
        x2, y2 = points[j]
        area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        max_area = max(max_area, area)

print(f"Part 1: {max_area}")

# Part 2: Rectangle must be inside the rectilinear polygon
# The polygon edges alternate between horizontal and vertical
# Build the polygon edges
n = len(points)
edges = []
for i in range(n):
    p1 = points[i]
    p2 = points[(i + 1) % n]
    edges.append((p1, p2))

# For a rectangle with corners (x_min, y_min) to (x_max, y_max) to be inside the polygon,
# all four corners must be inside, AND no edge of the polygon can cross through the rectangle

def point_in_polygon(px, py):
    """Ray casting: count crossings of ray going right from point"""
    crossings = 0
    for (x1, y1), (x2, y2) in edges:
        if x1 == x2:  # vertical edge
            # Ray goes right from (px, py), crosses vertical edge at x=x1 if:
            # - edge is to the right of point (x1 > px)
            # - point's y is between edge's y values
            if x1 > px and min(y1, y2) <= py < max(y1, y2):
                crossings += 1
    return crossings % 2 == 1

def segment_intersects_rect(x1, y1, x2, y2, rx_min, ry_min, rx_max, ry_max):
    """Check if a line segment intersects the interior of a rectangle (not just boundary)"""
    if x1 == x2:  # vertical segment
        # Check if the segment passes through the rectangle's interior
        seg_y_min, seg_y_max = min(y1, y2), max(y1, y2)
        # Segment must cross the rectangle horizontally (x in interior)
        if rx_min < x1 < rx_max:
            # And have y overlap with rectangle
            if seg_y_min < ry_max and seg_y_max > ry_min:
                return True
    else:  # horizontal segment (y1 == y2)
        seg_x_min, seg_x_max = min(x1, x2), max(x1, x2)
        # Segment must cross the rectangle vertically (y in interior)
        if ry_min < y1 < ry_max:
            # And have x overlap with rectangle
            if seg_x_min < rx_max and seg_x_max > rx_min:
                return True
    return False

def rectangle_in_polygon(rx_min, ry_min, rx_max, ry_max):
    """Check if rectangle is entirely inside the polygon"""
    # Check all 4 corners are inside or on boundary
    corners = [(rx_min, ry_min), (rx_min, ry_max), (rx_max, ry_min), (rx_max, ry_max)]

    # For corners that are red tiles, they're on boundary - that's fine
    # For other corners, they must be strictly inside
    points_set = set(points)
    for cx, cy in corners:
        if (cx, cy) not in points_set:
            if not point_in_polygon(cx, cy):
                return False

    # Check no polygon edge crosses through the rectangle's interior
    for (x1, y1), (x2, y2) in edges:
        if segment_intersects_rect(x1, y1, x2, y2, rx_min, ry_min, rx_max, ry_max):
            return False

    return True

# Find largest valid rectangle
max_area2 = 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        x1, y1 = points[i]
        x2, y2 = points[j]
        rx_min, rx_max = min(x1, x2), max(x1, x2)
        ry_min, ry_max = min(y1, y2), max(y1, y2)

        if rectangle_in_polygon(rx_min, ry_min, rx_max, ry_max):
            area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
            max_area2 = max(max_area2, area)

print(f"Part 2: {max_area2}")
