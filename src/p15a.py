import re
from sympy import Interval, Union

PATTERN = re.compile(
    r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")


def main(filename, row_to_inspect):
    deadzone_intervals = []
    beacon_locations = []
    with open(filename) as fd:
        for line in fd:
            match = PATTERN.match(line.strip())
            sx, sy, bx, by = map(int, match.groups())
            if by == row_to_inspect:
                beacon_locations.append(Interval.Ropen(bx, bx + 1))
            l1_radius = abs(sx - bx) + abs(sy - by)

            vd_from_row = abs(sy - row_to_inspect)
            if l1_radius < vd_from_row:
                continue

            deadzone_start = sx - (l1_radius - vd_from_row)
            deadzone_end = sx + (l1_radius - vd_from_row) + 1
            deadzone_intervals.append(
                Interval.Ropen(deadzone_start, deadzone_end))

    deadzone = Union(*deadzone_intervals) - Union(*beacon_locations)
    print(deadzone)
    print(deadzone.measure)


if __name__ == '__main__':
    import sys
    main(sys.argv[1], int(sys.argv[2]))
