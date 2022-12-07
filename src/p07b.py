# python src/p07b.py data/p07.txt

from functools import cached_property
import sys

class Node:
    def __init__(self, name: str, size: int, parent=None):
        self.name = name
        self.size = size # size = 0 -> directory
        self.parent = parent
        self.children = {} # for convenience, files also have children

    def add_child(self, name, size):
        self.children[name] = Node(name, size, parent=self)

    @cached_property
    def total_size(self):
        return sum((node.total_size for node in self.children.values()), self.size)
    
    def walk(self):
        yield self
        for child in self.children.values():
            yield from child.walk()

class Filesystem:
    def __init__(self) -> None:
        self.root = self.current = Node("", 0)

    def cd(self, arg):
        if arg == "/":
            target = self.root
        elif arg == "..":
            target = self.current.parent
        else:
            target = self.current.children[arg]
        self.current = target

    def ingest_ls_result(self, result_line):
        size_str, name = result_line.split(" ")
        if size_str == "dir":
            size = 0
        else:
            size = int(size_str)
        self.current.add_child(name, size)


fs = Filesystem()
with open(sys.argv[1]) as fd:
    line = next(fd).strip()
    while True:
        try:
            assert line.startswith("$")
            command = line[2:]
            if command == "ls":
                while True:
                    line = next(fd).strip()
                    if line.startswith("$"):
                        break
                    else:
                        fs.ingest_ls_result(line)
            else:
                assert command.startswith("cd ")
                cd_arg = command[3:]
                fs.cd(cd_arg)
                line = next(fd).strip()
        except StopIteration:
            break

total_size = 70000000
occupied_size = fs.root.total_size
unused_size_target = 30000000
space_needed_to_free_up = unused_size_target - (total_size - fs.root.total_size)

print(min(node.total_size for node in fs.root.walk() if node.total_size >= space_needed_to_free_up))