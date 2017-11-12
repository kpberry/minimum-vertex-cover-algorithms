def read_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        file.readline()
        for i, line in enumerate(file):
            if len(line.strip()) > 0:
                # 1 indexing because this is matlab apparently
                graph[i] = set(int(i) - 1 for i in line.split())
    return graph
