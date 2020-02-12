class Grid(dict):
    def __repr__(self):
        min_x = min(x for x, y in self.keys())
        max_x = max(x for x, y in self.keys())
        # width = max_x - min_x
        min_y = min(y for x, y in self.keys())
        max_y = max(y for x, y in self.keys())
        out = ""
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                char = self.get((x, y), " ")
                out += char
            out += "\n"
        # out += ' ' * (width)
        return out


actions = {
    "R": lambda x, y: (x + 1, y),
    "L": lambda x, y: (x - 1, y),
    "U": lambda x, y: (x, y + 1),
    "D": lambda x, y: (x, y - 1),
}


class Point:
    def __init__(self, marker, **metadata):
        self.marker = marker
        self.__dict__.update(metadata)

    def __repr__(self):
        return self.marker


def draw_grid(wire):
    grid = Grid()
    current_location = (0, 0)
    total_distance = 0
    for instruction in wire:
        direction, distance = instruction[0], int(instruction[1:])
        func = actions[direction]
        for i in range(distance):
            total_distance += 1
            current_location = func(*current_location)
            if direction in "LR" and not grid.get(current_location):
                grid[current_location] = Point("-", distance=total_distance)
            elif direction in "UD" and not grid.get(current_location):
                grid[current_location] = Point("|", distance=total_distance)
        grid[current_location] = Point("+")
    return grid


def manhattan_distance(x, y, grids):
    return abs(x) + abs(y)


def total_distance(x, y, grids):
    return sum(grid[x, y].distance for grid in grids)


def find_intersection(wires, metric):
    grids = [draw_grid(wire) for wire in wires]
    intersections = set(grids[0].keys()).intersection(grids[1].keys())

    distances = [(metric(pos[0], pos[1], grids), pos) for pos in intersections]
    closest = sorted(distances)[0]
    return closest


wires1 = [["R8", "U5", "L5", "D3"], ["U7", "R6", "D4", "L4"]]


wires2 = [
    ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
    ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"],
]

wires3 = [
    ["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"],
    ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"],
]

wires = [line.split(",") for line in open("input.txt")]

print(find_intersection(wires1, manhattan_distance))
print(find_intersection(wires2, manhattan_distance))
print(find_intersection(wires3, manhattan_distance))
print(find_intersection(wires, manhattan_distance))


print(find_intersection(wires1, total_distance))
print(find_intersection(wires2, total_distance))
print(find_intersection(wires3, total_distance))
print(find_intersection(wires, total_distance))
