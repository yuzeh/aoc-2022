import sys

class CircuitWatcher:
    total_signal_strength = 0

    def cycle_start(self, circuit):
        if circuit.cycle_number in {20, 60, 100, 140, 180, 220}:
            self.total_signal_strength += circuit.cycle_number * circuit.x


class ClockCircuit:
    cycle_number = 0
    x = 1

    def __init__(self, circuit_watcher) -> None:
        self._circuit_watcher = circuit_watcher
    
    def start_new_cycle(self):
        self.cycle_number += 1
        self._circuit_watcher.cycle_start(self)

    def addx(self, v):
        self.start_new_cycle()
        self.start_new_cycle()
        self.x += v
    
    def noop(self):
        self.start_new_cycle()


def main(filename):
    watcher = CircuitWatcher()
    circuit = ClockCircuit(watcher)

    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if line == 'noop':
                circuit.noop()
            else:
                addx, v = line.split(" ")
                assert addx == 'addx'
                circuit.addx(int(v))
    
    print(watcher.total_signal_strength)


if __name__ == '__main__':
    main(sys.argv[1])