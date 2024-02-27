from config import *


def calculate_distance(node1, node2):
    return np.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def calculate_total_distance(path, nodes):
    total_distance = sum(calculate_distance(nodes[path[i]], nodes[path[i + 1]]) for i in range(len(path) - 1))
    total_distance += calculate_distance(nodes[path[-1]], nodes[path[0]])  # Return to the starting point
    return total_distance


def create_distance_matrix(nodes):
    num_nodes = len(nodes)
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            distance_matrix[i][j] = calculate_distance(nodes[i], nodes[j])
            distance_matrix[j][i] = distance_matrix[i][j]
    return distance_matrix


def initialize_population(size, num_nodes):
    return [random.sample(range(num_nodes), num_nodes) for _ in range(size)]


def select_parents(population, distances, nodes):
    distances_values = [calculate_total_distance(path, nodes) for path in population]
    selected_indices = np.argsort(distances_values)[:2]
    return [population[i] for i in selected_indices]


def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + [node for node in parent2 if node not in parent1[:crossover_point]]
    return child


def mutate(child, mutation_rate):
    if random.random() < mutation_rate:
        indices = random.sample(range(len(child)), 2)
        child[indices[0]], child[indices[1]] = child[indices[1]], child[indices[0]]
    return child


def genetic_algorithm(nodes, population_size=pop_size, generations=gens, mutation_rate=mut_rate):
    num_nodes = len(nodes)
    distance_matrix = create_distance_matrix(nodes)
    population = initialize_population(population_size, num_nodes)

    for generation in range(generations):
        parents = select_parents(population, distance_matrix, nodes)
        offspring = [crossover(parents[0], parents[1]) for _ in range(population_size - 2)]
        offspring = [mutate(child, mutation_rate) for child in offspring]
        population = parents + offspring

        best_path = min(population, key=lambda path: calculate_total_distance(path, nodes))
        best_distance = calculate_total_distance(best_path, nodes)

        # print(f"Generation {generation + 1}: Best Path = {best_path}, Best Distance = {best_distance}")

    best_path = min(population, key=lambda path: calculate_total_distance(path, nodes))
    best_distance = calculate_total_distance(best_path, nodes)

    return best_path, best_distance
