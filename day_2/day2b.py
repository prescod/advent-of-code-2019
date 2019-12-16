from operator import add, mul


def process(operator, address1, address2, target_address, memory):
    operand1 = memory[address1]
    operand2 = memory[address2]
    # print(operator, (address1, address2), (operand1, operand2), target_address, memory)
    memory[target_address] = operator(operand1, operand2)


opcodes = {1: add, 2: mul}


def compute(memory, position):
    opcode = None
    opcode = memory[position]
    while opcode != 99:
        process(
            opcodes[opcode],
            memory[position + 1],
            memory[position + 2],
            memory[position + 3],
            memory,
        )
        position = position + 4
        opcode = memory[position]


memory = [int(x) for x in open("day2.txt").read().split(",")]


def do_computation(clean_tape):
    for noun in range(0, 99):
        for verb in range(0, 99):
            memory = clean_tape[:]
            memory[1] = noun
            memory[2] = verb

            compute(memory, 0)

            if memory[0] == 19690720:
                print(noun * 100 + verb)


do_computation(memory)
