from intcomputer import Computer
from collections import defaultdict


program = [int(x) for x in open("day13.txt").read().split(",")]
program[0] = 2
working_memory = defaultdict(int, enumerate(program))

blocks = []


class Console:
    def __init__(self):
        self.buffer = []
        self.everything = []
        self.grid = {}
        self.score = 0
        self.ball_pos = 0
        self.paddle_pos = 0

    def output(self, num):
        buffer = self.buffer
        self.everything.append(num)
        buffer.append(num)
        if len(buffer) == 3:
            if buffer[0] == -1 and buffer[1] == 0:
                self.score = buffer[2]
            else:
                self.grid[buffer[0], buffer[1]] = buffer[2]
            self.buffer = []

    def print_grid(self):
        out = "\n\n\n"
        width = max(x for x, y in self.grid.keys())
        height = max(y for x, y in self.grid.keys())
        for y in range(0, height):
            for x in range(0, width):
                value = self.grid.get((x, y), 0)
                if value == 0:
                    char = " "
                elif value == 1:
                    char = "O"
                elif value == 2:
                    char = "X"
                elif value == 3:
                    char = "_"
                    self.paddle_pos = x
                elif value == 4:
                    char = "o"
                    self.ball_pos = x
                out += char
            out += "\n"
        out += ' '* (width//2)
        out += str(self.score)
        print(out)
        import time
        time.sleep(0.1)

    def input(self):
        while 1:
            if self.ball_pos > self.paddle_pos:
                yield 1
            elif self.ball_pos == self.paddle_pos:
                yield 0
            else:
                yield -1
            self.print_grid()
            # input("Command? ")


con = Console()
c = Computer(working_memory, con.input(), con.output)
c.compute()

print(con.everything[-30:])
