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

    def __eq__(self, other):
        return not self != other

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
    with open(filename) as fd:
        lines = [line.strip() for line in fd]
    p1s = [Signal.from_list(eval(line)) for line in lines[0::3]]
    p2s = [Signal.from_list(eval(line)) for line in lines[1::3]]

    divider_1 = Signal.from_list([[2]])
    divider_2 = Signal.from_list([[6]])

    signals = p1s + p2s + divider_1 + divider_2
    sorted_signals = list(sorted(signals))

    divider_1_index = -1
    divider_2_index = -1
    for index, signal in enumerate(sorted_signals, start=1):
        if signal == divider_1:
            divider_1_index = index
        if signal == divider_2:
            divider_2_index = index

    print(divider_1_index * divider_2_index)


if __name__ == '__main__':
    main(sys.argv[1])
