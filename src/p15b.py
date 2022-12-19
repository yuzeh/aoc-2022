import re
from shapely import Polygon, Point

PATTERN = re.compile(
    r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")


def main(filename, max_coord):
    base_polygon = Polygon([
        (0, 0),
        (0, max_coord),
        (max_coord, max_coord),
        (max_coord, 0)
    ])
    poly = base_polygon
    with open(filename) as fd:
        for line in fd:
            match = PATTERN.match(line.strip())
            sx, sy, bx, by = map(int, match.groups())
            l1_radius = abs(sx - bx) + abs(sy - by)

            left = (sx - l1_radius - 0.75, sy)
            top = (sx, sy + l1_radius + 0.75)
            right = (sx + l1_radius + 0.75, sy)
            bottom = (sx, sy - l1_radius - 0.75)

            poly -= Polygon([left, top, right, bottom])

    print(poly.centroid)
    print(poly.centroid.x * 4000000 + poly.centroid.y)


if __name__ == '__main__':
    import sys
    main(sys.argv[1], int(sys.argv[2]))
