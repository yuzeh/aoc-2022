# python src/p05a.py data/p05.txt

import sys
import re
from typing import List


class Stacks:
    def __init__(self, stacks: List[List[str]]):
        self.stacks = stacks

    def move(self, num, from_, to):
        for i in range(num):
            self.move_one(from_, to)

    def move_one(self, from_, to):
        item = self.stacks[from_ - 1].pop(0)
        self.stacks[to - 1].insert(0, item)

    def print_tops(self):
        return ''.join(stack[0] for stack in self.stacks)

def read_current_stacks(fd):
    lines = []
    for line in fd:
        if not line.strip():
            break
        lines.append(line[1::4])
    lines = lines[:-1]
    stacks = [[line[i] for line in lines if line[i] != ' '] for i in range(len(lines[0]))]
    return Stacks(stacks)

instruction_regex = re.compile(r"^move (\d+) from (\d+) to (\d+)$")

if __name__ == '__main__':
    with open(sys.argv[1]) as fd:
        stacks = read_current_stacks(fd)
        for instruction in fd:
            match = instruction_regex.match(instruction)
            stacks.move(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    print(stacks.print_tops())
