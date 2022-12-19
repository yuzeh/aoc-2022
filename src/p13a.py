import sys


class Signal(list):
    def __lt__(self, other) -> bool:
        if isinstance(other, int):
            other = Signal([other])

        for self_item, other_item in zip(self, other):
            if isinstance(self_item, int) and isinstance(other_item, int):
                pass
            elif isinstance(self_item, Signal) and isinstance(other_item, int):
                other_item = Signal([other_item])
            elif isinstance(self_item, int) and isinstance(other_item, Signal):
                self_item = Signal([self_item])
            elif isinstance(self_item, Signal) and isinstance(other_item, Signal):
                pass
            else:
                raise ValueError("hmm")

            if self_item < other_item:
                return True
            elif self_item > other_item:
                return False
            else:
                continue

        return len(self) < len(other)

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self

    @classmethod
    def from_list(cls, l):
        items = cls()
        for item in l:
            if isinstance(item, list):
                items.append(cls.from_list(item))
            else:
                items.append(item)
        return items


def main(filename):
    index_sum = 0
    current_index = 1
    with open(filename) as fd:
        lines = [line.strip() for line in fd]
        p1s = [Signal.from_list(eval(line)) for line in lines[0::3]]
        p2s = [Signal.from_list(eval(line)) for line in lines[1::3]]

        for current_index, (p1, p2) in enumerate(zip(p1s, p2s), start=1):
            if p1 < p2:
                index_sum += current_index

    print(index_sum)


if __name__ == '__main__':
    main(sys.argv[1])
