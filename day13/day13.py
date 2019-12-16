from intcomputer import Computer
from collections import defaultdict


program = [int(x) for x in open("day13.txt").read().split(",")]
working_memory = defaultdict(int, enumerate(program))

blocks = []

c = Computer(working_memory, iter([2]), blocks.append)
c.compute()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

grid = {}

for x, y, typ in chunks(blocks, 3):
    grid[x,y] = typ

print(len([a for a in grid.values() if a == 2]))
