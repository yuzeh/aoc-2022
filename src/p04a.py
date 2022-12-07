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
    
def read_interval(value: str) -> Interval:
    lo_str, hi_str = value.split("-")
    return Interval(int(lo_str), int(hi_str))

def read_interval_pair(value: str):
    left, right = value.split(",")
    return read_interval(left), read_interval(right)

if __name__ == '__main__':
    fully_contain_count = 0
    with open(sys.argv[1]) as fd:
        for line in fd:
            left, right = read_interval_pair(line.strip())
            if left.contains(right) or right.contains(left):
                fully_contain_count += 1
    print(fully_contain_count)