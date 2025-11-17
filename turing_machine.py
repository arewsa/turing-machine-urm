class State:
    def __init__(self, rules: dict[str, tuple[str, int, 'State']]):
        self.rules: dict[str, tuple[str, int, str]] = rules

class TuringMachine:
    def __init__(self, initial_state: str, tape: str, states: dict[str, State], head: int = 0):
        self.state: str = initial_state
        self.tape: dict[int, str] = {i: tape[i] for i in range(len(tape))}
        self.head: int = head
        self.states: dict[str, State] = states

    def run(self):
        while self.state != 'halt':
            self.step()

    def step(self):
        current_symbol = self.tape[self.head]
        new_symbol, direction, self.state = self.states[self.state].rules[current_symbol]
        self.tape[self.head] = new_symbol
        self.head += direction
        if self.head not in self.tape:
            self.tape[self.head] = '0'

    def print_tape(self):
        print(''.join(self.tape[key] for key in sorted(self.tape.keys())))
        print(' ' * (self.head - min(self.tape.keys())) + '^' + ' ' * (max(self.tape.keys()) - self.head))

    def print_count_of_ones(self):
        print(sum(1 for value in self.tape.values() if value == '1'))

