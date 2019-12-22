from operator import add, mul


def process(operator, address1, address2, target_address, memory):
    operand1 = memory[address1]
    operand2 = memory[address2]
    print(operator, (address1, address2),
          (operand1, operand2), target_address, memory)
    memory[target_address] = operator(operand1, operand2)


opcodes = {1: add, 2: mul}


def compute(memory, position):
    opcode = memory[position]
    while opcode != 99:
        if opcode in opcodes:
            process(
                opcodes[opcode],
                memory[position + 1],
                memory[position + 2],
                memory[position + 3],
                memory,
            )
        else:
            assert 0, (opcode, opcodes)
        print(memory)
        position = position + 4
        opcode = memory[position]


memory = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
memory = [1, 0, 0, 0, 99]
memory = [2, 3, 0, 3, 99]
memory = [2, 4, 4, 5, 99, 0]
memory = [1, 1, 1, 4, 99, 5, 6, 0, 99]

memory = [int(x) for x in open("day2.txt").read().split(",")]

memory[1] = 12
memory[2] = 2


compute(memory, 0)

print(memory[0])
