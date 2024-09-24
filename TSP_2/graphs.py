import random
from config import WIDTH, GRAPH_HEIGHT

def create_dense_graph(num_nodes):
    nodes = [(random.randint(50, WIDTH - 50), random.randint(50, GRAPH_HEIGHT - 50)) for _ in range(num_nodes)]
    lines_data = [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]
    return nodes, lines_data

def create_sparse_graph(num_nodes):
    nodes = [(random.randint(50, WIDTH - 50), random.randint(50, GRAPH_HEIGHT - 50)) for _ in range(num_nodes)]
    lines_data = []
    for i in range(num_nodes):
        num_edges = random.randint(1, 4)
        edges = random.sample(range(num_nodes), num_edges)
        for edge in edges:
            if edge != i and (i, edge) not in lines_data and (edge, i) not in lines_data:
                lines_data.append((i, edge))
    return nodes, lines_data

def find_farthest_nodes(nodes, min_distance_nodes=5):
    max_distance = 0
    start_node = 0
    end_node = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            distance = ((nodes[i][0] - nodes[j][0]) ** 2 + (nodes[i][1] - nodes[j][1]) ** 2) ** 0.5
            if distance > max_distance:
                max_distance = distance
                start_node = i
                end_node = j
    return start_node, end_node
