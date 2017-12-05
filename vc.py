# Small utility functions for the vertex cover problem.
# The eval_fitness function bases the fitness on the number of covered edges
# by a vertex cover vs. the number of vertices that the vertex cover uses, with
# a negative penalty for larger vertex covers.

def is_solution(graph, vc):
    # A VC is a solution if and only if each edge has at least one endpoint in
    # the vertex cover.
    for u in graph:
        for v in graph[u]:
            if vc[u] + vc[v] == 0:
                return False
    return True


def eval_fitness(graph, vc):
    # get the total number of edges to cover vs. the number covered by vc
    covered_edges = 0
    marked = [False] * len(vc)
    # Make sure that edges aren't double counted by marking both endpoints
    # upon counting the edge so that it isn't counted again
    for u in graph:
        if not marked[u]:
            for v in graph[u]:
                if not marked[v]:
                    if vc[u] + vc[v] > 0:
                        covered_edges += 1
                        marked[u] = True
                        marked[v] = True
    # Compute the quality of the vc (add len(vc) to make sure it's positive)
    return covered_edges - sum(vc) + len(vc)
