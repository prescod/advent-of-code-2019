from pprint import pprint
import networkx
from networkx.algorithms.shortest_paths.generic import shortest_path


def paths_to_COM(node, COM):
    return len()


def checksum(f):
    graph = networkx.Graph()
    for line in f:
        parent, satellite = line.strip().split(")")
        graph.add_edge(satellite, parent)
    path = shortest_path(graph, source="YOU", target="SAN")
    return len(path) - 3


with open("input.txt") as f:
    pprint(checksum(f))
