from pydantic import BaseModel
import regex as re

class URM(BaseModel):
    """Unlimited Register Machine (URM) implementation for computable functions."""

    def __init__(self, registers: str, program: list[str]):
        """
        Initialize a URM with initial register values and a program.
        
        Args:
            registers: Space-separated string of initial register values (e.g., "3 4 5")
            program: List of instruction strings in format "OP(params)" (e.g., ["Z(1)", "S(2)"])
        """
        registers_dict = {i+1: int(registers.split(" ")[i]) for i in range(len(registers.split()))}

        super().__init__(registers=registers_dict, program=program)

    registers: dict[int, int]
    program: list[str]
    current_instruction_index: int = 1

    def zero(self, register_index: int):
        """
        Zero operation: set the specified register to 0.
        
        Args:
            register_index: Index of the register to zero (1-indexed)
        """
        if register_index not in self.registers:
            self.registers[register_index] = 0
        self.registers[register_index] = 0
        self.current_instruction_index += 1

    def add_one(self, register_index: int):
        """
        Successor operation: increment the specified register by 1.
        
        Args:
            register_index: Index of the register to increment (1-indexed)
        """
        if register_index not in self.registers:
            self.registers[register_index] = 0
        self.registers[register_index] += 1
        self.current_instruction_index += 1

    def transfer(self, source_register_index: int, destination_register_index: int):
        """
        Transfer operation: copy value from source register to destination register.
        
        Args:
            source_register_index: Index of the source register (1-indexed)
            destination_register_index: Index of the destination register (1-indexed)
        """
        if source_register_index not in self.registers:
            self.registers[source_register_index] = 0
        if destination_register_index not in self.registers:
            self.registers[destination_register_index] = 0
        self.registers[destination_register_index] = self.registers[source_register_index]
        self.current_instruction_index += 1

    def conditional_jump(self, first_register_index: int, second_register_index: int, index_of_next_instruction: int):
        """
        Jump operation: conditionally jump to another instruction.
        
        If the values in the two registers are equal, jump to the specified instruction index.
        Otherwise, continue to the next instruction.
        
        Args:
            first_register_index: Index of the first register to compare (1-indexed)
            second_register_index: Index of the second register to compare (1-indexed)
            index_of_next_instruction: Instruction index to jump to if registers are equal (1-indexed)
        """
        if first_register_index not in self.registers:
            self.registers[first_register_index] = 0
        if second_register_index not in self.registers:
            self.registers[second_register_index] = 0
        if self.registers[first_register_index] == self.registers[second_register_index]:
            self.current_instruction_index = index_of_next_instruction
        else:
            self.current_instruction_index += 1

    def read_instruction(self):
        """
        Read and execute the current instruction from the program.
        
        Parses instruction strings in format "OP(params)" where OP is Z, S, T, or J.
        Automatically calls the appropriate operation method.
        
        Raises:
            ValueError: If instruction format is invalid or parameter count is incorrect
        """
        match = re.match(r'^([ZSTJ])\((\d+(?:,\s*\d+)*)\)$', self.program[self.current_instruction_index - 1])
        if not match:
            raise ValueError(f"Invalid instruction format: {self.program[self.current_instruction_index]}")
    
        op_type = match.group(1)
        params_str = match.group(2)
        params = [int(p.strip()) for p in params_str.split(',')]
        
        if op_type == 'Z':
            if len(params) != 1:
                raise ValueError(f"Z requires 1 parameter, got {len(params)}")
            self.zero(*params)
        
        elif op_type == 'S':
            if len(params) != 1:
                raise ValueError(f"S requires 1 parameter, got {len(params)}")
            self.add_one(*params)
        
        elif op_type == 'T':
            if len(params) != 2:
                raise ValueError(f"T requires 2 parameters, got {len(params)}")
            self.transfer(*params)
        
        elif op_type == 'J':
            if len(params) != 3:
                raise ValueError(f"J requires 3 parameters, got {len(params)}")
            self.conditional_jump(*params)
        
        else:
            raise ValueError(f"Unknown operation: {op_type}")

    def run(self):
        """
        Execute the URM program from start to finish.
        
        Runs all instructions sequentially until the program ends.
        """
        while self.current_instruction_index <= len(self.program):
            self.read_instruction()

    def run_and_print_per_step(self):
        """
        Execute the program with step-by-step output for debugging.
        
        Prints register state, current instruction, and instruction index before and after each step.
        """
        while self.current_instruction_index <= len(self.program):
            print(self.registers)
            print(self.program[self.current_instruction_index - 1])
            print(self.current_instruction_index)
            self.read_instruction()
            print(self.registers)
            print("-" * 10)
        