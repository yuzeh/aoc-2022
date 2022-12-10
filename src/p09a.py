class Position:
    x = 0
    y = 0

    def astuple(self):
        return self.x, self.y

def main(filename):
    tail_positions = set()
    head = Position()
    tail = Position()

    def step(direction):
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
        
        # Resolve tail
        dx = head.x - tail.x    # tail.x + dx = head.x
        dy = head.y - tail.y    # tail.y + dy = head.y
        if abs(dx) <= 1 and abs(dy) <= 1:
            pass
        elif dx == 0:
            tail.y += dy / abs(dy)
        elif dy == 0:
            tail.x += dx / abs(dx)
        else:
            tail.y += dy / abs(dy)
            tail.x += dx / abs(dx)
    
    def record_tail():
        tail_positions.add(tail.astuple())

    with open(filename) as fd:
        for line in fd:
            direction, distance_str = line.split(" ")
            for _ in range(int(distance_str)):
                step(direction)
                record_tail()
    
    print(len(tail_positions))


if __name__ == '__main__':
    import sys
    main(sys.argv[1])