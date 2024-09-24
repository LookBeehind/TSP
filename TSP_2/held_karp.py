# held_karp.py

from config import euclidean_distance

def held_karp(nodes, lines_data):
    num_nodes = len(nodes)
    all_nodes = set(range(num_nodes))
    memo = {}
    path_table = {}
    num_iterations = [0]

    def tsp_helper(current, remaining):
        num_iterations[0] += 1
        if not remaining:
            return euclidean_distance(nodes[current], nodes[0])

        if (current, tuple(remaining)) in memo:
            return memo[(current, tuple(remaining))]

        min_distance = float('inf')
        next_node_choice = None

        for next_node in remaining:
            if (current, next_node) in lines_data or (next_node, current) in lines_data:
                new_remaining = tuple(node for node in remaining if node != next_node)
                distance = euclidean_distance(nodes[current], nodes[next_node]) + tsp_helper(next_node, new_remaining)
                if distance < min_distance:
                    min_distance = distance
                    next_node_choice = next_node

        memo[(current, tuple(remaining))] = min_distance
        path_table[(current, tuple(remaining))] = next_node_choice
        return min_distance

    optimal_distance = tsp_helper(0, all_nodes - {0})

    path = [0]
    current = 0
    remaining = all_nodes - {0}

    while remaining:
        next_node = path_table.get((current, tuple(remaining)), None)
        if next_node is None:
            print(f"Ошибка: не найден следующий узел для текущего узла {current} с оставшимися узлами {remaining}")
            break
        path.append(next_node)
        current = next_node
        remaining.remove(next_node)

    return path, optimal_distance, num_iterations[0]
