# A set of utility functions for manipulating sparse adjacency matrices as
# graphs. We have chosen not to use classes in order to avoid the significant
# overhead of class instantiation and method calls in Python.

from itertools import chain


# Read an input grahp into a sparse adjacency matrix line by line.
def read_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        file.readline()
        for i, line in enumerate(file):
            # Increment our counter, but do not make a vertex if there are no
            # neighbors on the line; this is because isolated vertices have no
            # edges and do not matter for the vertex cover.
            if len(line.strip()) > 0:
                # 1 indexing because this is matlab apparently
                # Makes everything 0 indexed like in real programming languages
                graph[i] = set(int(i) - 1 for i in line.split())
    return graph


# Copies a graph vertex by vertex.
def copy_graph(graph):
    return {u: set(v for v in graph[u]) for u in graph}


# Gets all of the edges in a graph without duplicates or reversed edges
def get_edges(graph):
    return list(set(chain(
        *[[(u, v) if u < v else (v, u) for v in graph[u]] for u in graph]
    )))


# Remove a set of numbered vertices in a graph, including the edges of those
# vertices.
def remove_vertices(graph, vertices):
    return {u: set(v for v in graph[u] if not v in vertices) for u in graph if
            not u in vertices}


# Remove isolated vertices in a graph (vertices with no edges)
def remove_isolates(graph):
    return {u: set(v for v in graph[u] if len(graph[v]) > 0) for u in graph if
            len(graph[u]) > 0}
