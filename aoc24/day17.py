from aoc24 import day_data
from dataclasses import dataclass, field
from enum import Enum
import re
from typing import List
from itertools import zip_longest

TEST_INPUT = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

TEST_INPUT_B = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

program_re = re.compile(r"""Register A: (\d+)
Register B: (\d+)
Register C: (\d+)

Program: (.*)""", re.MULTILINE)

def parse(data_source):
    a, b, c, program = program_re.match(day_data(data_source).text()).groups()
    return Machine(int(a), int(b), int(c), 0, [int(x) for x in program.split(",")])

class Instruction(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

@dataclass
class Machine:
    a: int
    b: int
    c: int
    ip: int = 0
    program: List[int] = field(default_factory=list)
    output: List[int] = field(default_factory=list)

    def run(self):
        """
        >>> m = Machine(0, 0, 9, 0, [2, 6])
        >>> m.run()
        >>> m.b
        1
        >>> m = Machine(10, 0, 0, 0, [5,0,5,1,5,4])
        >>> m.run()
        >>> m.output
        [0, 1, 2]
        >>> m = Machine(2024, 0, 0, 0, [0,1,5,4,3,0])
        >>> m.run()
        >>> m.output
        [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
        >>> m.a
        0
        >>> m = Machine(0, 29, 0, 0, [1, 7])
        >>> m.run()
        >>> m.b
        26
        >>> m = Machine(0, 2024, 43690, 0, [4, 0])
        >>> m.run()
        >>> m.b
        44354
        """
        while self.ip in range(len(self.program)):
            self.step()

    def run_to_next_output(self):
        while self.ip in range(len(self.program)):
            output = self.step()
            if output is not None:
                return output
        return None

    def step(self):
        instruction = Instruction(self.program[self.ip])
        operand = self.program[self.ip + 1]
        match instruction:
            case Instruction.ADV:
                return self.adv(operand)
            case Instruction.BXL:
                return self.bxl(operand)
            case Instruction.BST:
                return self.bst(operand)
            case Instruction.JNZ:
                return self.jnz(operand)
            case Instruction.BXC:
                return self.bxc(operand)
            case Instruction.OUT:
                return self.out(operand)
            case Instruction.BDV:
                return self.bdv(operand)
            case Instruction.CDV:
                return self.cdv(operand)

    
    def combo(self, operand):
        match operand:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise ValueError("Invalid operand")
            case x:
                return x

    def adv(self, operand):
        self.a = self.a >> self.combo(operand)
        self.ip += 2

    def bxl(self, operand):
        self.b = self.b ^ operand
        self.ip += 2

    def bst(self, operand):
        self.b = self.combo(operand) % 8
        self.ip += 2

    def jnz(self, operand):
        if self.a != 0:
            self.ip = operand
        else:
            self.ip += 2

    def bxc(self, operand):
        self.b = self.b ^ self.c
        self.ip += 2

    def out(self, operand):
        output = self.combo(operand) % 8
        self.output.append(output)
        self.ip += 2
        return output

    def bdv(self, operand):
        self.b = self.a >> self.combo(operand)
        self.ip += 2

    def cdv(self, operand):
        self.c = self.a >> self.combo(operand)
        self.ip += 2


def day15a(machine):
    """
    >>> day15a(parse(TEST_INPUT))
    '4,6,3,5,6,3,5,2,1,0'
    """
    machine.run()
    return ",".join(str(i) for i in machine.output)

def find(revtarget, a, f):
    """All the relevant programs shift a right by 3 and compute an
    output independent of b and c, and end with a = 0. So we can work
    backwards considering 8 possibilities each time and checking which
    will produce the correct output.
    """
    if revtarget == []:
        return a
    else:
        next_output = revtarget[0]
        rest = revtarget[1:]
        candidates = [apre for apre in range(a << 3, (a << 3) + 8) if f(apre) == next_output]
        for c in candidates:
            r = find(rest, c, f)
            if r is not None:
                return r

def day15b(machine):
    """
    >>> day15b(parse(TEST_INPUT_B))
    117440
    """
    revtarget = machine.program[::-1]

    def f(a):
        machine.a = a
        machine.b = 0
        machine.c = 0
        machine.ip = 0
        return machine.run_to_next_output()

    return find(revtarget, 0, f)

def main():
    machine = parse(17)
    print(f"Day 15a: {day15a(machine)}")
    print(f"Day 15b: {day15b(machine)}")


if __name__ == "__main__":
    main()
