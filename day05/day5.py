import operator
from functools import partial
from dataclasses import dataclass

ADDRESS_MODE = 0
IMMEDIATE_MODE = 1


def binary_operator(operator, computer, mode1=0, mode2=0):
    operand1 = computer.read(1, mode1)
    operand2 = computer.read(2, mode2)
    computer.write(3, operator(operand1, operand2))
    computer.advance(4)


add = partial(binary_operator, operator.add)


mul = partial(binary_operator, operator.mul)


lt = partial(binary_operator, operator.lt)


eq = partial(binary_operator, operator.eq)


def inp(computer):
    value = next(computer.stdin)
    computer.write(1, value)
    computer.advance(2)


def outp(computer, mode1=0):
    val_address = computer.read(1, mode1)
    computer.stdout(val_address)
    computer.advance(2)


def jump_if_true(computer, mode1=0, mode2=0):
    if computer.read(1, mode1):
        computer.jump(computer.read(2, mode2))
    else:
        computer.advance(3)


def jump_if_false(computer, mode1=0, mode2=0):
    cond = computer.read(1, mode1)
    if not cond:
        computer.jump(computer.read(2, mode2))
    else:
        computer.advance(3)


opcodes = {
    1: add,
    2: mul,
    3: inp,
    4: outp,
    5: jump_if_true,
    6: jump_if_false,
    7: lt,
    8: eq,
}


def opcode_modes(opcode):
    real_opcode = opcode % 100
    modeflags = opcode // 100
    modes = []
    while modeflags:
        modes.append(modeflags % 10)
        modeflags = modeflags // 10
    assert real_opcode in opcodes, opcode
    return real_opcode, modes


@dataclass
class Computer:
    memory: list = None
    stdin: None = None
    stdout: None = None
    position: int = 0
    relative_base: int = 0

    def advance(self, positions: int):
        self.position += positions

    def read(self, num, mode):
        value = self.memory[self.position + num]
        if mode == IMMEDIATE_MODE:
            return value
        else:
            return self.memory[value]

    def write(self, num, value):
        address = self.memory[self.position + num]
        self.memory[address] = value

    def jump(self, address):
        self.position = address

    def compute(self):
        opcode = None
        opcode = self.memory[self.position]
        while opcode != 99:
            real_opcode, modes = opcode_modes(opcode)
            print(real_opcode, modes, opcode, self.memory)
            opcode_func = opcodes[real_opcode]
            opcode_func(self, *modes)
            opcode = self.memory[self.position]


program = [int(x) for x in open("day5.txt").read().split(",")]
# memory = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

c = Computer(program, iter([5]), print)
c.compute()
