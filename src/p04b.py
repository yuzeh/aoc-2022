# python src/p04a.py data/p04.txt

import sys

class Interval:
    def __init__(self, lo, hi):
        assert lo <= hi
        self.lo = lo
        self.hi = hi
    
    def contains(self, other):
        if not isinstance(other, Interval):
            raise ValueError(f"{other} must be an Interval")
        return self.lo <= other.lo and other.hi <= self.hi 
    
    def overlaps(self, other):
        "Is one of the endpoints contained in the other interval?"
        if not isinstance(other, Interval):
            raise ValueError(f"{other} must be an Interval")
        return (
            (self.lo <= other.lo and other.lo <= self.hi)
            or (self.lo <= other.hi and other.hi <= self.hi)
            or (other.lo <= self.lo and self.lo <= other.hi)
            or (other.lo <= self.hi and self.hi <= other.hi)
        )
    
def read_interval(value: str) -> Interval:
    lo_str, hi_str = value.split("-")
    return Interval(int(lo_str), int(hi_str))

def read_interval_pair(value: str):
    left, right = value.split(",")
    return read_interval(left), read_interval(right)

if __name__ == '__main__':
    overlap_count = 0
    with open(sys.argv[1]) as fd:
        for line in fd:
            left, right = read_interval_pair(line.strip())
            if left.overlaps(right):
                overlap_count += 1
    print(overlap_count)