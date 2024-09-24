from queue import PriorityQueue
from config import euclidean_distance

def a_star_algorithm(nodes, lines_data, start_node, end_node):
    num_nodes = len(nodes)
    open_set = PriorityQueue()
    open_set.put((0, start_node, [start_node], 0))
    g_score = {i: float('inf') for i in range(num_nodes)}
    g_score[start_node] = 0
    visited_states = set()

    best_path = None
    best_cost = float('inf')

    while not open_set.empty():
        _, current, path, cost = open_set.get()

        if (current, tuple(path)) in visited_states:
            continue
        visited_states.add((current, tuple(path)))

        if len(path) == num_nodes:
            path.append(start_node)
            total_distance = cost + euclidean_distance(nodes[current], nodes[start_node])
            if total_distance < best_cost:
                best_cost = total_distance
                best_path = path
            continue

        for neighbor in range(num_nodes):
            if (current, neighbor) in lines_data or (neighbor, current) in lines_data:
                if neighbor not in path:
                    tentative_g_score = cost + euclidean_distance(nodes[current], nodes[neighbor])
                    new_path = path + [neighbor]
                    if tentative_g_score < best_cost:
                        f_score = tentative_g_score + euclidean_distance(nodes[neighbor], nodes[start_node])
                        open_set.put((f_score, neighbor, new_path, tentative_g_score))

    return best_path if best_path else [], best_cost if best_path else float('inf'), len(visited_states)
