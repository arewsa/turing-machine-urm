from pydantic import BaseModel
import regex as re

class URM(BaseModel):

    def __init__(self, registers: str, program: list[str]):
        registers_dict = {i+1: int(registers.split(" ")[i]) for i in range(len(registers.split()))}

        super().__init__(registers=registers_dict, program=program)

    registers: dict[int, int]
    program: list[str]
    current_instruction_index: int = 1


    def zero(self, register_index: int):
        if register_index not in self.registers:
            self.registers[register_index] = 0
        self.registers[register_index] = 0
        self.current_instruction_index += 1

    
    def add_one(self, register_index: int):
        if register_index not in self.registers:
            self.registers[register_index] = 0
        self.registers[register_index] += 1
        self.current_instruction_index += 1

    def transfer(self, destination_register_index: int, source_register_index: int):
        if source_register_index not in self.registers:
            self.registers[source_register_index] = 0
        self.registers[destination_register_index] = self.registers[source_register_index]
        self.current_instruction_index += 1

    def conditional_jump(self, first_register_index: int, second_register_index: int, index_of_next_instruction: int):
        if first_register_index not in self.registers:
            self.registers[first_register_index] = 0
        if second_register_index not in self.registers:
            self.registers[second_register_index] = 0
        if self.registers[first_register_index] == self.registers[second_register_index]:
            self.current_instruction_index = index_of_next_instruction
        else:
            self.current_instruction_index += 1

    def read_instruction(self):
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
        while self.current_instruction_index <= len(self.program):
            self.read_instruction()

    def run_and_print_per_step(self):
        while self.current_instruction_index <= len(self.program):
            print(self.registers)
            print(self.program[self.current_instruction_index - 1])
            print(self.current_instruction_index)
            self.read_instruction()
            print(self.registers)
            print("-" * 10)
        