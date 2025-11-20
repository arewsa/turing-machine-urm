# Computational Models Implementation

This project implements two fundamental computational models: **Turing Machine** and **Unlimited Register Machine (URM)**. Both models are equivalent in computational power and can compute the same class of functions (Church-Turing thesis).

## Table of Contents

- [Turing Machine](#turing-machine)
- [Unlimited Register Machine (URM)](#unlimited-register-machine-urm)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
- [Sharing the Project](#sharing-the-project)

## Turing Machine

A Turing machine is a theoretical computational model with an infinite tape and a read/write head that can move left or right. It consists of states and transition rules that define how the machine processes input.

### Basic Usage

```python
from computational_models import State, TuringMachine

# Define states with transition rules
# Format: {input_symbol: (output_symbol, direction, next_state)}
# direction: 1 = right, -1 = left, 0 = stay
states = {
    'q1': State({
        '0': ('1', 1, 'q1'),    # Read '0', write '1', move right, go to q1
        '1': ('0', -1, 'q2'),   # Read '1', write '0', move left, go to q2
    }),
    'q2': State({
        '0': ('0', 0, 'halt'),  # Read '0', write '0', stay, halt
        '1': ('1', 1, 'q1'),     # Read '1', write '1', move right, go to q1
    }),
    'halt': State({})  # Halt state (no transitions)
}

# Create machine with initial tape and state
machine = TuringMachine(
    initial_state='q1',
    tape='101',
    states=states,
    head=0  # Optional: initial head position
)

# Run the machine
machine.run()

# Inspect results
machine.print_tape()           # Print tape with head position
machine.print_count_of_ones() # Count '1' symbols (useful for unary numbers)
```

### Methods

- **`run()`**: Executes the machine until it reaches the halt state
- **`step()`**: Executes a single step (read, write, move, change state)
- **`print_tape()`**: Displays the tape content with head position indicator
- **`print_count_of_ones()`**: Prints the count of '1' symbols (useful for unary representation)

### Example: Multiplication by 2

```python
# Multiply number by 2 in unary representation
# Input: "111" (number 3) -> Output: "111111" (number 6)

states = {
    "q1": State(
            {
                # If we see '0', we're done - halt
                "0": ("0", 0, "halt"),
                # If we see '1', mark it (write '0') and move left to find the end
                "1": ("0", -1, "q2"),
            }
        ),
        "q2": State(
            {
                # Found the end (empty cell) - add a new '1' and move right to return
                "0": ("1", 1, "q3"),
                # Continue moving left through existing '1's
                "1": ("1", -1, "q2"),
            }
        ),
        "q3": State(
            {
                # Found the marked position - restore it to '1' and move right to process next
                "0": ("1", 1, "q1"),
                # Continue moving right through existing '1's
                "1": ("1", 1, "q3"),
            }
        ),
}

machine = TuringMachine(initial_state='q1', tape='111', states=states)
machine.run()
machine.print_count_of_ones()  # Output: 6
```

## Unlimited Register Machine (URM)

A URM operates on an infinite sequence of registers, each storing a non-negative integer. It has four basic operations: Zero (Z), Successor (S), Transfer (T), and Jump (J).

### Basic Usage

```python
from computational_models import URM

# Initialize URM with registers and program
# Registers: space-separated initial values (1-indexed)
# Program: list of instructions in format "OP(params)"

urm = URM(
    registers="3 4 5",  # Register 1=3, Register 2=4, Register 3=5
    program=[
        "Z(1)",      # Zero register 1
        "S(2)",      # Increment register 2
        "T(2, 3)",   # Copy register 2 to register 3
        "J(1, 2, 0)" # Jump to instruction 0 if register 1 == register 2
    ]
)

# Execute the program
urm.run()

# Access results
print(urm.registers)  # {1: 0, 2: 5, 3: 5, ...}
```

### Instruction Format

- **Z(n)**: Zero operation - set register n to 0
- **S(n)**: Successor operation - increment register n by 1
- **T(m, n)**: Transfer operation - copy value from register m to register n
- **J(m, n, q)**: Jump operation - if register m == register n, jump to instruction q (1-indexed), otherwise continue to next instruction

### Methods

- **`run()`**: Executes the entire program from start to finish
- **`read_instruction()`**: Reads and executes the current instruction
- **`run_and_print_per_step()`**: Executes with step-by-step debugging output
- **`zero(register_index)`**: Sets register to 0
- **`add_one(register_index)`**: Increments register by 1
- **`transfer(source, destination)`**: Copies value between registers
- **`conditional_jump(r1, r2, instruction_index)`**: Conditional jump based on register comparison

### Example: Addition Function

```python
# Add two numbers: R1 + R2 -> R1 (result stored in R1)
# Input: registers="5 3" (R1=5, R2=3)
# Output: R1 will contain 8 (5 + 3)

urm = URM(
    registers="5 3 0",  # R1=5, R2=3, R3=0 (R3 is used as counter)
    program=[
        "J(3, 2, 5)",   # If counter R3 == R2, jump to end (instruction 5)
        "S(1)",         # Increment R1 (add 1 to the result)
        "S(3)",         # Increment counter R3
        "J(1, 1, 1)",   # Always true (R1 == R1), jump back to start (loop)
        "Z(3)"          # Zero the counter R3 (cleanup)
    ])

urm.run()
print(urm.registers[1])  # Output: 8
```

**Algorithm explanation:**
- R3 serves as a counter starting at 0
- Loop: while R3 < R2, increment both R1 and R3
- When R3 == R2, exit the loop
- Result: R1 has been incremented R2 times, so R1 = original_R1 + R2

### Debugging

Use `run_and_print_per_step()` to see the execution step by step:

```python
urm = URM(registers="2 3", program=["S(1)", "T(1, 2)"])
urm.run_and_print_per_step()
# Output shows register state before and after each instruction
```

## Installation

### Option 1: Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/arewsa/turing-machine-urm.git
cd turing-machine-urm

# Install dependencies and package
uv sync
uv pip install -e .

# Verify installation
python -c "from computational_models import TuringMachine, URM; print('Installed successfully!')"
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/arewsa/turing-machine-urm.git
cd turing-machine-urm

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Verify installation
python -c "from computational_models import TuringMachine, URM; print('Installed successfully!')"
```

### Option 3: Direct Installation from GitHub

```bash
# Install directly from GitHub
pip install git+https://github.com/arewsa/turing-machine-urm.git

# Or with uv
uv pip install git+https://github.com/arewsa/turing-machine-urm.git
```

## Quick Start

After installation, you can use the package like this:

```python
# Import the classes
from computational_models import TuringMachine, URM, State

# Use Turing Machine
states = {
    'q1': State({'0': ('0', 0, 'halt'), '1': ('1', 1, 'q1')})
}
machine = TuringMachine(initial_state='q1', tape='111', states=states)
machine.run()
machine.print_count_of_ones()

# Use URM
urm = URM(registers="5 3", program=["S(1)", "T(1, 2)"])
urm.run()
print(urm.registers)
```

## Examples

See the `tests/` directory for more examples:

- `test_turing.py`: Examples of Turing machine programs (multiplication by 2)
- `test_urm.py`: Examples of URM programs (addition, subtraction, division)

## Notes

- **Turing Machine**: Uses dictionary-based tape for efficient sparse representation
- **URM**: Registers are 1-indexed (first register is index 1)
- Both models support infinite memory (tape/registers extend automatically)
- Programs continue until halt state (Turing) or program end (URM)
- **Python 3.12+** required

