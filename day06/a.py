from pprint import pprint
import networkx
from networkx.algorithms.shortest_paths.generic import shortest_path


def paths_to_COM(node, COM):
    return len()


def checksum(f):
    graph = networkx.DiGraph()
    for line in f:
        parent, satellite = line.strip().split(")")
        graph.add_edge(satellite, parent)
    paths = shortest_path(graph, target="COM")
    return sum(len(path)-1 for path in paths.values())


with open("input.txt") as f:
    pprint(checksum(f))
