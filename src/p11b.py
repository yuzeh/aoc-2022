import math
import operator
import sys

class Monkey:
    def __init__(
        self,
        *,
        bus,
        id,
        starting_items,
        operation,
        test_divisible_by,
        test_true_toss_to_monkey,
        test_false_toss_to_monkey,
    ) -> None:
        self.bus = bus
        self.id = id
        self.held_items = starting_items
        self.operation = operation
        self.test_divisible_by = test_divisible_by
        self.test_true_toss_to_monkey = test_true_toss_to_monkey
        self.test_false_toss_to_monkey = test_false_toss_to_monkey

        self._num_items_inspected = 0
    
    def inspect_next_item(self):
        item_worry = self.held_items.pop(0)
        item_worry = self.operation(item_worry)
        # Divisibility test will still work if the worry of the item is modded by the
        # LCM of the individual monkey divisors:
        item_worry = item_worry % self.bus.monkey_divisors_lcm
        if item_worry % self.test_divisible_by == 0:
            self.bus.toss_to(self.test_true_toss_to_monkey, item_worry)
        else:
            self.bus.toss_to(self.test_false_toss_to_monkey, item_worry)
        self._num_items_inspected += 1

    def run_turn(self):
        while self.held_items:
            self.inspect_next_item()

    @property
    def num_items_inspected(self):
        return self._num_items_inspected

class MonkeyBus:
    index_to_monkey = {}

    def add_monkey(
        self,
        *,
        id,
        starting_items,
        operation,
        test_divisible_by,
        test_true_toss_to_monkey,
        test_false_toss_to_monkey,
    ):
        self.index_to_monkey[id] = Monkey(
            bus=self,
            id=id,
            starting_items=starting_items,
            operation=operation,
            test_divisible_by=test_divisible_by,
            test_true_toss_to_monkey=test_true_toss_to_monkey,
            test_false_toss_to_monkey=test_false_toss_to_monkey,
        )
    
    def run_round(self):
        indexes = sorted(list(self.index_to_monkey))
        for index in indexes:
            self.index_to_monkey[index].run_turn()
    
    def toss_to(self, monkey_id, item_worry):
        # print(f"Tossing item with worry {item_worry} to monkey {monkey_id}")
        self.index_to_monkey[monkey_id].held_items.append(item_worry)

    @property
    def monkey_divisors_lcm(self):
        return math.lcm(*[monkey.test_divisible_by for monkey in self.index_to_monkey.values()])

def parse_monkey(lines):
    monkey_constructor_kwargs = {}
    monkey_constructor_kwargs['id'] = int(lines[0][len('Monkey '):-1])

    starting_items_text = lines[1].split(': ')[1]
    monkey_constructor_kwargs['starting_items'] = [int(item_worry) for item_worry in starting_items_text.split(", ")]

    operation_text = lines[2].split(': ')[1]
    operation_tokens = operation_text.split(' ')
    operator = operation_to_operator(operation_tokens[3])
    if operation_tokens[4] == 'old':
        operation = lambda x: operator(x, x)
    else:
        operation = lambda x: operator(x, int(operation_tokens[4]))
    monkey_constructor_kwargs['operation'] = operation

    test_tokens = lines[3].split(': ')[1].split(' ')
    monkey_constructor_kwargs['test_divisible_by'] = int(test_tokens[2])

    if_true_tokens = lines[4].split(': ')[1].split(' ')
    monkey_constructor_kwargs['test_true_toss_to_monkey'] = int(if_true_tokens[3])

    if_false_tokens = lines[5].split(': ')[1].split(' ')
    monkey_constructor_kwargs['test_false_toss_to_monkey'] = int(if_false_tokens[3])

    return monkey_constructor_kwargs

def operation_to_operator(operation):
    if operation == '*':
        return operator.mul
    if operation == '+':
        return operator.add
    
    raise ValueError(f"Unknown operation: {operation}")


def main(filename):
    monkey_constructors = []
    current_monkey_lines = []
    with open(filename) as fd:
        for line in fd:
            line = line.rstrip()
            if not line.strip():
                monkey_constructors.append(parse_monkey(current_monkey_lines))
                current_monkey_lines = []
            else:
                current_monkey_lines.append(line)
    
    if current_monkey_lines:
        monkey_constructors.append(parse_monkey(current_monkey_lines))
    
    bus = MonkeyBus()
    for constructor in monkey_constructors:
        bus.add_monkey(**constructor)
    
    # for i in range(20):
    for i in range(10_000):
        bus.run_round()

    monkey_items_inspected = sorted([monkey.num_items_inspected for monkey in bus.index_to_monkey.values()])
    print(operator.mul(*monkey_items_inspected[-2:]))


if __name__ == '__main__':
    main(sys.argv[1])