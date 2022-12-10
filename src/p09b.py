N_ROPES = 10

class Position:
    x = 0
    y = 0

    def astuple(self):
        return self.x, self.y

def main(filename):
    tail_positions = set()
    positions = [Position() for i in range(N_ROPES)]
    head = positions[0]
    tail = positions[-1]

    def step_head(direction):
        # Resolve head
        if direction == "L":
            head.x -= 1
        elif direction == "R":
            head.x += 1
        elif direction == "U":
            head.y += 1
        else:
            assert direction == "D"
            head.y -= 1
    
    def resolve_knot(idx):
        assert idx > 0
        curr = positions[idx]
        prev = positions[idx - 1]
        # Resolve tail
        dx = prev.x - curr.x    # curr.x + dx = prev.x
        dy = prev.y - curr.y    # curr.y + dy = prev.y
        if abs(dx) <= 1 and abs(dy) <= 1:
            pass
        elif dx == 0:
            curr.y += dy / abs(dy)
        elif dy == 0:
            curr.x += dx / abs(dx)
        else:
            curr.y += dy / abs(dy)
            curr.x += dx / abs(dx)
    
    def record_tail():
        tail_positions.add(tail.astuple())

    with open(filename) as fd:
        for line in fd:
            direction, distance_str = line.split(" ")
            for _ in range(int(distance_str)):
                step_head(direction)
                for idx in range(1, N_ROPES):
                    resolve_knot(idx)
                record_tail()
    
    print(len(tail_positions))


if __name__ == '__main__':
    import sys
    main(sys.argv[1])