import operator
from functools import partial
from dataclasses import dataclass
from pysnooper import snoop

ADDRESS_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2


def binary_operator(operator, computer, mode1=0, mode2=0, mode3=0):
    operand1 = computer.read(1, mode1)
    operand2 = computer.read(2, mode2)
    computer.write(3, operator(operand1, operand2), mode3)
    computer.advance(4)


def add(*args):
    return binary_operator(operator.add, *args)


def mul(*args):
    return binary_operator(operator.mul, *args)


def lt(*args):
    return binary_operator(operator.lt, *args)


def eq(*args):
    return binary_operator(operator.eq, *args)


def inp(computer, mode1=0):
    value = next(computer.stdin)
    assert mode1 != 1
    computer.write(1, value, mode1)
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


def adjust_relative_base(computer, mode1=0):
    computer.relative_base += computer.read(1, mode1)
    computer.advance(2)


opcodes = {
    1: add,
    2: mul,
    3: inp,
    4: outp,
    5: jump_if_true,
    6: jump_if_false,
    7: lt,
    8: eq,
    9: adjust_relative_base,
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
        elif mode == RELATIVE_MODE:
            return self.memory[self.relative_base + value]
        else:
            return self.memory[value]

    def write(self, num, value, mode):
        assert mode != IMMEDIATE_MODE
        address_operand = self.memory[self.position + num]
        if mode == RELATIVE_MODE:
            address = address_operand + self.relative_base
        else:
            address = address_operand
        self.memory[address] = value

    def jump(self, address):
        self.position = address

    def compute(self):
        opcode = None
        opcode = self.memory[self.position]
        while opcode != 99:
            real_opcode, modes = opcode_modes(opcode)
            opcode_func = opcodes[real_opcode]
            opcode_func(self, *modes)
            opcode = self.memory[self.position]
