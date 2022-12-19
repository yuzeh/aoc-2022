import dataclasses


@dataclasses.dataclass
class RockPoint:
    x: int
    y: int

    def iter_points_to(self, other):
        assert isinstance(other, RockPoint)
        if other.x == self.x:
            moving_dimension = 'y'
            static_dimension = 'x'
        else:
            moving_dimension = 'x'
            static_dimension = 'y'

        if getattr(self, moving_dimension) < getattr(other, moving_dimension):
            start = self
            end = other
        else:
            start = other
            end = self

        static_dim_value = getattr(self, static_dimension)
        for moving_dim_value in range(getattr(start, moving_dimension), getattr(end, moving_dimension) + 1):
            kwargs = {moving_dimension: moving_dim_value,
                      static_dimension: static_dim_value}
            yield RockPoint(**kwargs)


class Grid:
    coords = {}
    min_rock_x = None
    max_rock_x = None

    def draw_rock(self, rock_path):
        """Fills in the rock path in the grid.

        Done before we start dripping sand.
        """
        for i in range(len(rock_path) - 1):
            for point in rock_path[i].iter_points_to(rock_path[i + 1]):
                self.coords[point.x, point.y] = '#'
                if self.min_rock_x is None or self.min_rock_x > point.x:
                    self.min_rock_x = point.x
                if self.max_rock_x is None or self.max_rock_x < point.x:
                    self.max_rock_x = point.x

    def drip_sand(self):
        """Simulates one unit of sand dropping through from 500,0 onto the grid.

        Returns True if the sand finally rests, False if not.
        """
        sx, sy = 500, 0
        while True:
            # if we've escaped the bounds of the map then we're gonna fall forever
            if sx < self.min_rock_x or sx > self.max_rock_x:
                return False

            if self.point_at(sx, sy + 1) is None:  # check below
                sy += 1
                continue
            elif self.point_at(sx - 1, sy + 1) is None:  # check below-left
                sx -= 1
                sy += 1
                continue
            elif self.point_at(sx + 1, sy + 1) is None:  # check below-right
                sx += 1
                sy += 1
                continue
            else:
                self.coords[sx, sy] = 'o'
                return True

    def point_at(self, x, y):
        return self.coords.get((x, y))


def main(filename):
    grid = Grid()

    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            rock_points = []
            for coord in line.split(' -> '):
                x, y = coord.split(",")
                rock_points.append(RockPoint(int(x), int(y)))
            grid.draw_rock(rock_points)

    sand_count = 0
    while grid.drip_sand():
        sand_count += 1

    print(sand_count)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
