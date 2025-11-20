class State:
    """Represents a state in a Turing machine with transition rules."""
    
    def __init__(self, rules: dict[str, tuple[str, int, 'State']]):
        """
        Initialize a state with transition rules.
        
        Args:
            rules: Dictionary mapping input symbols to (output_symbol, direction, next_state)
                   where direction is 1 (right), -1 (left), or 0 (stay)
        """
        self.rules: dict[str, tuple[str, int, str]] = rules

class TuringMachine:
    """Turing machine implementation with infinite tape and state transitions."""
    
    def __init__(self, initial_state: str, tape: str, states: dict[str, State], head: int = 0):
        """
        Initialize a Turing machine.
        
        Args:
            initial_state: Name of the starting state
            tape: Initial tape content as a string
            states: Dictionary mapping state names to State objects
            head: Initial position of the read/write head (default: 0)
        """
        self.state: str = initial_state
        self.tape: dict[int, str] = {i: tape[i] for i in range(len(tape))}
        self.head: int = head
        self.states: dict[str, State] = states

    def run(self):
        """Execute the Turing machine until it reaches the halt state."""
        while self.state != 'halt':
            self.step()

    def step(self):
        """
        Execute a single step of the Turing machine.
        
        Reads the current symbol, applies the transition rule, writes the new symbol,
        moves the head, and updates the state. Automatically extends the tape if needed.
        """
        current_symbol = self.tape[self.head]
        new_symbol, direction, self.state = self.states[self.state].rules[current_symbol]
        self.tape[self.head] = new_symbol
        self.head += direction
        if self.head not in self.tape:
            self.tape[self.head] = '0'

    def print_tape(self):
        """
        Print the current tape content with the head position indicator.
        
        Displays the tape as a string and marks the current head position with '^'.
        """
        print(''.join(self.tape[key] for key in sorted(self.tape.keys())))
        print(' ' * (self.head - min(self.tape.keys())) + '^' + ' ' * (max(self.tape.keys()) - self.head))

    def print_count_of_ones(self):
        """
        Print the count of '1' symbols on the tape.
        
        Useful for unary number representation where the count represents the number.
        """
        print(sum(1 for value in self.tape.values() if value == '1'))

