from config import *

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def held_karp(coordinates):
    num_nodes = len(coordinates)
    all_nodes = set(range(num_nodes))

    # Initialize memoization table and path reconstruction table
    memo = {}
    path_table = {}

    # Helper function for recursive calls
    def tsp_helper(current, remaining):
        if not remaining:
            return euclidean_distance(coordinates[current], coordinates[0])

        # Check if solution for this subproblem is already computed
        if (current, tuple(remaining)) in memo:
            return memo[(current, tuple(remaining))]

        min_distance = float('inf')
        next_node_choice = None

        for next_node in remaining:
            new_remaining = tuple(node for node in remaining if node != next_node)
            distance = euclidean_distance(coordinates[current], coordinates[next_node]) + tsp_helper(next_node, new_remaining)

            if distance < min_distance:
                min_distance = distance
                next_node_choice = next_node

        # Memoize the solution and update path table
        memo[(current, tuple(remaining))] = min_distance
        path_table[(current, tuple(remaining))] = next_node_choice

        return min_distance

    # Start the recursion from the first node
    optimal_distance = tsp_helper(0, all_nodes - {0})

    # Reconstruct the best path
    path = [0]
    current = 0
    remaining = all_nodes - {0}

    while remaining:
        next_node = path_table[(current, tuple(remaining))]
        path.append(next_node)
        current = next_node
        remaining.remove(next_node)

    return path, optimal_distance
