from config import *


def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def total_distance(path, coordinates):
    distance = 0
    for i in range(len(path) - 1):
        distance += euclidean_distance(coordinates[path[i]], coordinates[path[i + 1]])
    return distance


def a_star(coordinates):
    num_nodes = len(coordinates)
    all_nodes = set(range(num_nodes))
    start_node = 0

    priority_queue = [(0, start_node, tuple([start_node]))]
    num_iterations = 0

    while priority_queue:
        cost, current_node, path = heapq.heappop(priority_queue)
        num_iterations += 1

        if len(path) == num_nodes:
            # Completed the cycle, return to the starting node
            path += (start_node,)
            return path[1:], total_distance(path, coordinates), num_iterations

        for next_node in all_nodes - set(path):
            new_path = path + (next_node,)
            new_cost = total_distance(new_path, coordinates) + euclidean_distance(
                coordinates[next_node], coordinates[start_node]
            )

            heapq.heappush(priority_queue, (new_cost, next_node, new_path))

    return None, float('inf'), num_iterations  # No valid path found

