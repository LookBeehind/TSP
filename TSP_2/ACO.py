# ACO.py

import random
import numpy as np
from config import euclidean_distance, calculate_total_distance

def aco_algorithm(nodes, lines_data, start_node, num_ants=10, num_iterations=100, alpha=1, beta=2, evaporation_rate=0.5):
    num_nodes = len(nodes)
    pheromone_levels = np.ones((num_nodes, num_nodes))
    best_path = None
    best_distance = float('inf')
    best_iteration = 0

    def calculate_visibility():
        visibility = np.zeros((num_nodes, num_nodes))
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j and ((i, j) in lines_data or (j, i) in lines_data):
                    visibility[i][j] = 1 / euclidean_distance(nodes[i], nodes[j])
        return visibility

    visibility = calculate_visibility()

    for iteration in range(num_iterations):
        all_paths = []
        all_distances = []

        for _ in range(num_ants):
            path = [start_node]
            visited = set(path)
            while len(visited) < num_nodes:
                current = path[-1]
                probabilities = []
                total_prob = 0
                for next_node in range(num_nodes):
                    if next_node not in visited and ((current, next_node) in lines_data or (next_node, current) in lines_data):
                        prob = (pheromone_levels[current][next_node] ** alpha) * (visibility[current][next_node] ** beta)
                        total_prob += prob
                        probabilities.append((next_node, prob))
                if not probabilities:
                    break
                probabilities = [(node, prob / total_prob) for node, prob in probabilities]
                next_node = random.choices([node for node, _ in probabilities], [prob for _, prob in probabilities])[0]
                path.append(next_node)
                visited.add(next_node)

            if len(visited) == num_nodes:
                path.append(start_node)  # Return to the start node
                all_paths.append(path)
                distance = calculate_total_distance(path, nodes)
                all_distances.append(distance)
                if distance < best_distance:
                    best_distance = distance
                    best_path = path
                    best_iteration = iteration

        pheromone_levels *= (1 - evaporation_rate)
        for path, distance in zip(all_paths, all_distances):
            pheromone_deposit = 1 / distance
            for i in range(len(path) - 1):
                pheromone_levels[path[i]][path[i + 1]] += pheromone_deposit
                pheromone_levels[path[i + 1]][path[i]] += pheromone_deposit

        best_iteration = 100

    return best_path, best_distance, best_iteration
