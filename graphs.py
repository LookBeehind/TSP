from ACO import *
from A_star import *
from held_karp import *


class Graphs:

    def __init__(self):
        self.current_nodes = []
        self.current_trees = []
        self.current_city_images = []
        self.current_tree_images = []
        self.best_path = []
        self.best_distance = 0

    @staticmethod
    def generate_random_coordinates(n):
        coordinates = []
        for _ in range(n):
            x = random.randint(NODE_RADIUS, WIDTH - NODE_RADIUS)
            y = random.randint(NODE_RADIUS, HEIGHT - NODE_RADIUS)
            coordinates.append((x, y))
        return coordinates

    def draw_graph(self, new_screen, nodes, show_lines=True):
        new_screen.fill(GREEN)
        self.current_city_images = []
        self.current_tree_images = []
        for i in range(len(nodes)):
            node_position = nodes[i]

            # Load the city images
            city_number = random.randint(1, 5)
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

        trees = self.generate_random_coordinates(16)
        for tree in trees:
            tree_number = random.randint(1, 7)
            self.current_tree_images.append(f"assets/tree{tree_number}.png")
            tree_image = pygame.image.load(f"assets/tree{tree_number}.png")
            screen.blit(tree_image, tree)

        self.current_trees = trees
        self.current_nodes = nodes

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

    def draw_shortest_path(self, algorithm):
        if algorithm == 1:
            self.best_path, self.best_distance = genetic_algorithm(self.current_nodes)
        elif algorithm == 2:
            self.best_path, self.best_distance = a_star(self.current_nodes)
        elif algorithm == 3:
            self.best_path, self.best_distance = held_karp(self.current_nodes)

        screen.fill(GREEN)
        self.draw_roads()

        for i in range(len(self.current_nodes)):
            node_position = self.current_nodes[i]

            # Load the city image
            path = self.current_city_images[i]
            city_image = pygame.image.load(path)

            # Get the rectangle of the city image
            city_rect = city_image.get_rect()

            # Set the center of the rectangle to the node position
            city_rect.center = node_position

            # Blit the city image onto the screen at the center of the node position
            screen.blit(city_image, city_rect)

        trees = self.current_trees
        for index, tree in enumerate(trees):
            path = self.current_tree_images[index]
            tree_image = pygame.image.load(path)
            screen.blit(tree_image, tree)

        font = pygame.font.SysFont(None, 18)  # You can choose a font and size
        text = font.render(f"Best Distance: {self.best_distance}", True, (0, 0, 0))
        screen.blit(text, (10, 10))  # Adjust the position as needed

        pygame.display.flip()
