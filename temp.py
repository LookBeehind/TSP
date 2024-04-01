import numpy as np
import random
import pygame

class GeneticAlgorithm:
    def __init__(self):
        pass

    def calculate_distance(self, node1, node2):
        return np.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

    def calculate_total_distance(self, path, nodes):
        total_distance = sum(self.calculate_distance(nodes[path[i]], nodes[path[i + 1]]) for i in range(len(path) - 1))
        total_distance += self.calculate_distance(nodes[path[-1]], nodes[path[0]])  # Return to the starting point
        return total_distance

    def create_distance_matrix(self, nodes, graph_type='dense'):
        num_nodes = len(nodes)
        distance_matrix = np.zeros((num_nodes, num_nodes))
        if graph_type == 'dense':
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    distance_matrix[i][j] = self.calculate_distance(nodes[i], nodes[j])
                    distance_matrix[j][i] = distance_matrix[i][j]
        elif graph_type == 'sparse':
            # Randomly connect 50% of the nodes
            connected_nodes = random.sample(range(num_nodes), k=num_nodes // 2)
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if i in connected_nodes and j in connected_nodes:
                        distance_matrix[i][j] = self.calculate_distance(nodes[i], nodes[j])
                        distance_matrix[j][i] = distance_matrix[i][j]
        return distance_matrix

    def initialize_population(self, size, num_nodes):
        return [random.sample(range(num_nodes), num_nodes) for _ in range(size)]

    def select_parents(self, population, distances, nodes):
        distances_values = [self.calculate_total_distance(path, nodes) for path in population]
        selected_indices = np.argsort(distances_values)[:2]
        return [population[i] for i in selected_indices]

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(parent1) - 1)
        child = parent1[:crossover_point] + [node for node in parent2 if node not in parent1[:crossover_point]]
        return child

    def mutate(self, child, mutation_rate):
        if random.random() < mutation_rate:
            indices = random.sample(range(len(child)), 2)
            child[indices[0]], child[indices[1]] = child[indices[1]], child[indices[0]]
        return child

    def genetic_algorithm(self, nodes, graph_type='dense', population_size=10, generations=100, mutation_rate=0.01):
        num_nodes = len(nodes)
        distance_matrix = self.create_distance_matrix(nodes, graph_type)
        population = self.initialize_population(population_size, num_nodes)
        iteration_counter = 0

        for generation in range(generations):
            iteration_counter += 1  # Increment the iteration counter
            parents = self.select_parents(population, distance_matrix, nodes)
            offspring = [self.crossover(parents[0], parents[1]) for _ in range(population_size - 2)]
            offspring = [self.mutate(child, mutation_rate) for child in offspring]
            population = parents + offspring

            best_path = min(population, key=lambda path: self.calculate_total_distance(path, nodes))
            best_distance = self.calculate_total_distance(best_path, nodes)

            # Display code here

        best_path = min(population, key=lambda path: self.calculate_total_distance(path, nodes))
        best_distance = self.calculate_total_distance(best_path, nodes)

        return best_path, best_distance, iteration_counter

# Example usage:
nodes = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]  # Example node coordinates
ga = GeneticAlgorithm()
best_path, best_distance, iterations = ga.genetic_algorithm(nodes, graph_type='sparse')
print("Best Path:", best_path)
print("Best Distance:", best_distance)
print("Iterations:", iterations)
