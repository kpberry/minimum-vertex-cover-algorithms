from itertools import chain


def read_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        file.readline()
        for i, line in enumerate(file):
            if len(line.strip()) > 0:
                # 1 indexing because this is matlab apparently
                graph[i] = set(int(i) - 1 for i in line.split())
    return graph


def copy_graph(graph):
    return {u: set(v for v in graph[u]) for u in graph}


def get_edges(graph):
    return list(set(chain(
        *[[(u, v) if u < v else (v, u) for v in graph[u]] for u in graph]
    )))


def remove_vertices(graph, vertices):
    return {u: set(v for v in graph[u] if not v in vertices) for u in graph if
            not u in vertices}


def remove_isolates(graph):
    return {u: set(v for v in graph[u] if len(graph[v]) > 0) for u in graph if
            len(graph[u]) > 0}


if __name__ == '__main__':
    g = read_graph('./data/Data/karate.graph')
    print(len(get_edges(g)))
