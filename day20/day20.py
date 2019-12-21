import re
import string
import networkx
from networkx.algorithms.shortest_paths.generic import shortest_path


class Map:
    def build_map(self, cells):
        self.map = map = {}
        self.portals = portals = {}
        self.connections = networkx.Graph()

        for rownum, row in enumerate(cells, 1):
            for columnnum, cell in enumerate(row, 1):
                map[(columnnum, rownum)] = cell

        for (x, y), val in map.items():
            if val in string.ascii_letters:
                above = map.get((x, y-1))
                left = map.get((x-1, y))
                if above and above in string.ascii_letters:
                    label = above + val
                    below = map.get((x, y+1))
                    if below == ".":
                        portal_entrance = (x, y+1)
                    else:
                        print(above, val, x, y)
                        assert map.get((x, y-2)) == ".", (x, y-2)
                        portal_entrance = (x, y-2)
                    self.register_portal(portal_entrance, label)
                    map[portal_entrance] = "&"
                elif left and left in string.ascii_letters:
                    print(left, val, (x, y))
                    label = left + val
                    right = map.get((x+1, y))
                    if right == ".":
                        portal_entrance = (x+1, y)
                    else:
                        assert map.get((x-2, y)) == ".", (x-2, y)
                        portal_entrance = (x-2, y)
                    self.register_portal(portal_entrance, label)
                    map[portal_entrance] = "&"

    def register_portal(self, portal_entrance, label):
        self.portals[portal_entrance] = label
        self.portals.setdefault(label, []).append(portal_entrance)

    def connect_map(self):
        for cell, val in self.map.items():
            if val in (".", "&"):
                neighbours = self.adjacents(*cell)
                for neighbour in neighbours:
                    if self.map.get(neighbour) in (".", "&"):
                        self.connections.add_edge(cell, neighbour)
            if val == "&":
                portal_name = self.portals[cell]
                ends = self.portals[portal_name]
                assert cell in ends
                for other_end in ends:
                    if other_end != cell:
                        self.connections.add_edge(cell, other_end)

    def adjacents(self, x, y):
        return {(x+1, y), (x-1, y), (x, y+1), (x, y-1)}

    def draw(self):
        min_y = min(y for x, y in self.map)
        min_x = min(x for x, y in self.map)
        max_y = max(y for x, y in self.map)
        max_x = max(x for x, y in self.map)
        out = ""
        for i in range(min_y, max_y+1):
            for j in range(min_x, max_x+1):
                cell = self.map.get((j, i), " ")
                out += cell
            out += "\n"
        print(out)


def main():
    with open("input.txt") as input:
        lines = input.read().splitlines()
    cells = [char for char in (line for line in lines)]

    m = Map()
    m.build_map(cells)
    m.draw()
    m.connect_map()
    path = shortest_path(m.connections, m.portals["AA"][0], m.portals["ZZ"][0])
    print(path)
    print(len(path)-1)


main()
