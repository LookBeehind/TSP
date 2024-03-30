from ACO import *
from A_star import *
from held_karp import *


class Coordinates:

    def __init__(self):
        self.current_city_numbers = []
        self.current_tree_numbers = []
        self.current_tree_coordinates = []
        self.current_nodes = []

    @staticmethod
    def generate_random_coordinates(n):
        coordinates = []
        for _ in range(n):
            x = random.randint(NODE_RADIUS, WIDTH - NODE_RADIUS)
            y = random.randint(NODE_RADIUS, HEIGHT - NODE_RADIUS)
            coordinates.append((x, y))
        return coordinates

    def generate_random_cities(self, nodes):
        city_numbers = []
        for i in range(len(nodes)):
            city_number = random.randint(1, 5)
            city_numbers.append(city_number)
        self.current_city_numbers = city_numbers
        self.current_nodes = nodes
        return city_numbers

    def generate_random_trees(self):
        trees = self.generate_random_coordinates(16)
        tree_numbers = []
        tree_coords = []
        for tree in trees:
            tree_number = random.randint(1, 7)
            tree_numbers.append(tree_number)
            tree_coords.append(tree)
        self.current_tree_numbers = tree_numbers
        self.current_tree_coordinates = tree_coords
        return tree_numbers, tree_coords


class Graphs(Coordinates):

    def __init__(self):
        super().__init__()
        self.current_trees = []
        self.current_city_images = []
        self.current_tree_images = []
        self.best_path = []
        self.road_width = 0
        self.best_distance = 0
        self.iters = 0

    def draw_current_cities(self, new_screen, nodes, city_numbers, show_lines=True, final=False):
        new_screen.fill(GREEN)
        if final:
            self.draw_roads()

        for i in range(len(nodes)):
            node_position = nodes[i]

            # Load the city images
            city_number = city_numbers[i]
            self.current_city_images.append(f"assets/city{city_number}.png")
            city_image = pygame.image.load(f"assets/city{city_number}.png")

            # Get the rectangle of the city image
            city_rect = city_image.get_rect()

            # Set the center of the rectangle to the node position
            city_rect.center = node_position

            # Blit the city image onto the screen at the center of the node position
            screen.blit(city_image, city_rect)
            for j in range(i + 1, len(nodes)):
                if show_lines:
                    pygame.draw.line(new_screen, BLACK, nodes[i], nodes[j], 1)

    def draw_current_trees(self, tree_numbers, tree_coords, show_trees=True):
        for i, tree_coord in enumerate(tree_coords):
            tree_number = tree_numbers[i]
            self.current_tree_images.append(f"assets/tree{tree_number}.png")
            tree_image = pygame.image.load(f"assets/tree{tree_number}.png")
            if show_trees:
                screen.blit(tree_image, tree_coord)

    def draw_roads(self):
        # Draw custom roads with stripes
        stripe_width = 3  # Width of the stripes
        self.road_width = 10  # Width of the road

        for i in range(len(self.best_path) - 1):
            start_pos = self.current_nodes[self.best_path[i]]
            end_pos = self.current_nodes[self.best_path[i + 1]]

            # Draw the road
            pygame.draw.line(screen, GRAY, start_pos, end_pos, self.road_width)

            # Calculate the direction vector of the road
            direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])

            # Normalize the direction vector
            length = max(abs(direction[0]), abs(direction[1]))
            direction = (direction[0] / length, direction[1] / length)

            # Draw stripes along the road
            for j in range(0, length, 4 * stripe_width):
                stripe_start = (start_pos[0] + j * direction[0], start_pos[1] + j * direction[1])
                stripe_end = (
                start_pos[0] + (j + stripe_width) * direction[0], start_pos[1] + (j + stripe_width) * direction[1])

                pygame.draw.line(screen, WHITE, stripe_start, stripe_end, stripe_width)

        # Draw the road connecting the last and first nodes
        start_pos = self.current_nodes[self.best_path[-1]]
        end_pos = self.current_nodes[self.best_path[0]]

        pygame.draw.line(screen, GRAY, start_pos, end_pos, self.road_width)

        # Draw stripes along the road connecting the last and first nodes
        direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        length = max(abs(direction[0]), abs(direction[1]))
        direction = (direction[0] / length, direction[1] / length)

        for j in range(0, length, 4 * stripe_width):
            stripe_start = (start_pos[0] + j * direction[0], start_pos[1] + j * direction[1])
            stripe_end = (
                start_pos[0] + (j + stripe_width) * direction[0], start_pos[1] + (j + stripe_width) * direction[1])

            pygame.draw.line(screen, WHITE, stripe_start, stripe_end, stripe_width)

    @staticmethod
    def draw_lines(path, nodes):
        for i in range(len(path) - 1):
            pygame.draw.line(screen, BLACK, nodes[path[i]], nodes[path[i + 1]], 2)
        pygame.draw.line(screen, BLACK, nodes[path[-1]], nodes[path[0]], 2)

    def draw_shortest_path(self, algorithm):
        if algorithm == 1:
            self.best_path, self.best_distance, self.iters = self.genetic_algorithm(self.current_nodes)
        elif algorithm == 2:
            self.best_path, self.best_distance, self.iters = a_star(self.current_nodes)
        elif algorithm == 3:
            self.best_path, self.best_distance, self.iters = held_karp(self.current_nodes)

        self.draw_final_interface()

    def draw_final_interface(self):
        screen.fill(GREEN)

        self.draw_current_cities(screen, self.current_nodes, self.current_city_numbers, False, True)
        self.draw_current_trees(self.current_tree_numbers, self.current_tree_coordinates)

        self.draw_analyze(self.best_distance, self.iters)

    @staticmethod
    def draw_analyze(best_distance, iterations):
        font = pygame.font.SysFont(None, 30)  # You can choose a font and size
        distance = font.render(f"Best Distance: {best_distance}", True, (0, 0, 0))
        iterations = font.render(f"Iterations: {iterations}", True, (0, 0, 0))
        screen.blit(distance, (10, 10))  # Adjust the position as needed
        screen.blit(iterations, (10, 40))
        pygame.display.flip()

    def genetic_algorithm(self, nodes, population_size=pop_size, generations=gens, mutation_rate=mut_rate):
        num_nodes = len(nodes)
        distance_matrix = create_distance_matrix(nodes)
        population = initialize_population(population_size, num_nodes)
        iteration_counter = 0

        for generation in range(generations):
            iteration_counter += 1  # Increment the iteration counter
            parents = select_parents(population, distance_matrix, nodes)
            offspring = [crossover(parents[0], parents[1]) for _ in range(population_size - 2)]
            offspring = [mutate(child, mutation_rate) for child in offspring]
            population = parents + offspring

            best_path = min(population, key=lambda path: calculate_total_distance(path, nodes))
            best_distance = calculate_total_distance(best_path, nodes)

            self.draw_current_cities(screen, nodes, self.current_city_numbers, False)
            self.draw_current_trees(self.current_tree_numbers, self.current_tree_coordinates)
            self.draw_lines(best_path, nodes)
            self.draw_analyze(best_distance, iteration_counter)
            pygame.display.flip()

        best_path = min(population, key=lambda path: calculate_total_distance(path, nodes))
        best_distance = calculate_total_distance(best_path, nodes)

        return best_path, best_distance, iteration_counter
