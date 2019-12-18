from intcomputer import Computer
from collections import defaultdict
import random
import networkx
from networkx.algorithms.shortest_paths.generic import shortest_path

program = [int(x) for x in open("day15.txt").read().split(",")]
working_memory = defaultdict(int, enumerate(program))


NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4

# geography
WALL = "-"
SPACE = "."

# overlays
START = "+"
DROID = "o"
TREASURE = "x"


class Map:
    def __init__(self):
        self.droid_pos = (0, 0)
        self.locations = {(0,0): START}
        self.connections = networkx.Graph()
        self.connections.add_node((0,0))
        self.unexplored_spaces = {(0,0)}
        self.explored_spaces = {}
        self.target = (0,0)
        self.steps = []

    def draw(self):
        out = ""
        min_x = min(x for x, y in self.locations.keys())
        min_y = min(y for x, y in self.locations.keys())
        max_x = max(x for x, y in self.locations.keys())
        max_y = max(y for x, y in self.locations.keys())
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x,y)==self.droid_pos:
                    out += DROID
                elif (x,y)==(0,0):
                    out += START
                else:
                    typ = self.locations.get((x, y), " ")
                    out += typ
            out += "\n"
        print(out)

    def next_pos(self, command):
        x, y = self.droid_pos
        if command == NORTH:
            return (x, y - 1)
        elif command == SOUTH:
            return (x, y + 1)
        if command == WEST:
            return (x - 1, y)
        if command == EAST:
            return (x + 1, y)
        else:
            assert False, command

    def hit_wall(self, command):
        pos = self.next_pos(command)
        self.locations[pos] = WALL

    def moved_foward(self, command):
        pos = self.next_pos(command)
        self.locations[pos] = SPACE
        self.droid_pos = pos
        for neighbour in self.adjacents(pos):
            if self.locations.get(neighbour) == SPACE:
                self.connections.add_edge(self.droid_pos, neighbour)

    def found_treasure(self, command):
        self.moved_foward(command)
        self.treasure_pos = self.droid_pos
        print("FOUND TREASURE")
        self.draw()

    def next_step(self):
        if self.steps:  # on my way somewhere: keep going
            next_square = self.steps.pop(0)
            return self.direction_to_from_adjacent(self.droid_pos, next_square)

        unexplored_adjacents = [adj for adj in self.adjacents(self.droid_pos) 
                    if not adj in self.locations]

        # something local to look at
        if unexplored_adjacents:
            self.unexplored_spaces.add(self.droid_pos)
            return self.direction_to_from_adjacent(self.droid_pos, unexplored_adjacents[0])
        else:
            if self.droid_pos in self.unexplored_spaces:
                self.unexplored_spaces.remove(self.droid_pos)

        # better make a new plan!
        self.steps = list(self.find_shortest_path_to_unexplored(self.droid_pos))
        print("ZZZZ", self.steps)
        
        # and start executing it
        return self.next_step()

    def adjacents(self, loc):
        x, y = loc
        return {(x+1,y),(x-1,y),(x,y+1),(x,y-1)}

    def find_shortest_path_to_unexplored(self, pos):
        for visiting_node in networkx.bfs_tree(self.connections, pos):
            if visiting_node in self.unexplored_spaces:
                return shortest_path(pos, visiting_node)
        self.done()

    def direction_to_from_adjacent(self, current_pos, next_pos):
        print("XXX", current_pos, next_pos)
        if current_pos[0]<next_pos[0]:
            return EAST
        elif current_pos[0]>next_pos[0]:
            return WEST
        elif current_pos[1]<next_pos[1]:
            return SOUTH
        elif current_pos[1]>next_pos[1]:
            return NORTH
        assert 0, (current_pos, next_pos)

    def done(self):
        self.draw()
        path = shortest_path(self.connections, self.treasure_pos, (0,0))
        print("PATH", path)
        print("LENGTH", len(path))


class IO:
    def __init__(self):
        self.buffer = []
        self.map = Map()

    def input(self):
        potentials = []
        while 1:
            # target_node = self.map.find_nearest_incomplete()
            # if target_node == self.map.pos:
            #     for direction in range(1,5):
            #         target = self.map.next_pos(direction)
            #         symbol = self.map.locations.get(target)
            #         if not symbol:  # new location
            #             potentials = [direction]  # always prefer new locations
            #             # print("New", target, symbol)
            #             break
            #         elif symbol==SPACE:
            #             potentials.append(direction)
            #             # print("Retread", target, symbol)
            #         elif symbol==WALL:
            #             pass
            #         else:
            #             assert 0, symbol
            #     command = random.choice(potentials)
            # else:

            self.command = self.map.next_step()
            yield self.command

    def receive_output(self, value):
        if value == 0:
            self.map.hit_wall(self.command)
        elif value == 1:
            self.map.moved_foward(self.command)
        elif value == 2:
            self.map.found_treasure(self.command)
        self.buffer.append(value)


inputter = IO()

c = Computer(working_memory, inputter.input(), inputter.receive_output)
c.compute()

# 215 is too high