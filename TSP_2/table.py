import pygame
from config import GRAPH_HEIGHT, GRAY, WHITE, NODE_RADIUS, BLACK, BACKGROUND_COLOR
from background import background


class ResultTable:
    def __init__(self):
        self.rows = []

    def add_row(self, algorithm, path, best_distance, iteration, missing_edges):
        self.rows.append([algorithm, path, best_distance, iteration, missing_edges])

    def clear(self):
        self.rows = []

    def draw(self, screen):
        table_font = pygame.font.SysFont('Arial', 20)
        header_font = pygame.font.SysFont('Arial', 24)
        header = ['Algorithm', 'Best Path', 'Best Distance', 'Iteration', 'Edges not included']
        header_surface = header_font.render(' | '.join(header), True, WHITE)
        screen.blit(header_surface, (20, GRAPH_HEIGHT + 20))

        for i, row in enumerate(self.rows):
            row_surface = table_font.render(' | '.join(map(str, row)), True, WHITE)
            screen.blit(row_surface, (20, GRAPH_HEIGHT + 60 + i * 30))


def draw_roads(screen, nodes, best_path):
    stripe_width = 3  # Width of the stripes
    road_width = 10  # Width of the road

    for i in range(len(best_path) - 1):
        start_pos = nodes[best_path[i]]
        end_pos = nodes[best_path[i + 1]]

        # Draw the road
        pygame.draw.line(screen, GRAY, start_pos, end_pos, road_width)

        # Calculate the direction vector of the road
        direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])

        # Normalize the direction vector
        length = max(abs(direction[0]), abs(direction[1]))
        if length == 0:
            continue  # Skip drawing if length is zero
        direction = (direction[0] / length, direction[1] / length)

        # Draw stripes along the road
        for j in range(0, length, 4 * stripe_width):
            stripe_start = (start_pos[0] + j * direction[0], start_pos[1] + j * direction[1])
            stripe_end = (
                start_pos[0] + (j + stripe_width) * direction[0], start_pos[1] + (j + stripe_width) * direction[1])
            pygame.draw.line(screen, WHITE, stripe_start, stripe_end, stripe_width)

    # Draw the road connecting the last and first nodes
    start_pos = nodes[best_path[-1]]
    end_pos = nodes[best_path[0]]

    pygame.draw.line(screen, GRAY, start_pos, end_pos, road_width)

    # Draw stripes along the road connecting the last and first nodes
    direction = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    length = max(abs(direction[0]), abs(direction[1]))
    if length != 0:
        direction = (direction[0] / length, direction[1] / length)

        for j in range(0, length, 4 * stripe_width):
            stripe_start = (start_pos[0] + j * direction[0], start_pos[1] + j * direction[1])
            stripe_end = (
                start_pos[0] + (j + stripe_width) * direction[0], start_pos[1] + (j + stripe_width) * direction[1])
            pygame.draw.line(screen, WHITE, stripe_start, stripe_end, stripe_width)


def draw_path(screen, nodes, path, lines_data, best_distance, iteration, algorithm, start_img, dest_img, result_table,
              tree_imgs, node_font, start_node, end_node):
    screen.fill(BACKGROUND_COLOR)

    # Рисуем деревья на фоне
    background.draw_trees(screen)

    draw_roads(screen, nodes, path)

    for index, node in enumerate(nodes):
        if node[1] < GRAPH_HEIGHT:
            if index == start_node:
                screen.blit(start_img, (node[0] - start_img.get_width() // 2, node[1] - start_img.get_height() // 2))
            elif index == end_node:
                screen.blit(dest_img, (node[0] - dest_img.get_width() // 2, node[1] - dest_img.get_height() // 2))
            else:
                screen.blit(tree_imgs[0],
                            (node[0] - tree_imgs[0].get_width() // 2, node[1] - tree_imgs[0].get_height() // 2))
            text_surface = node_font.render(str(index), True, (255, 255, 255))
            screen.blit(text_surface, (node[0] + 5, node[1] + tree_imgs[0].get_height() // 2))

    result_table.add_row(algorithm, path, best_distance, iteration, [])
    result_table.draw(screen)
    pygame.display.flip()
