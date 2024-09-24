import pygame
import sys
import random
from config import num_nodes, FPS, WIDTH, HEIGHT, TABLE_HEIGHT, BACKGROUND_COLOR, CITY_IMAGE, START_IMAGE, DEST_IMAGE
from graphs import create_dense_graph, create_sparse_graph, find_farthest_nodes
from ACO import aco_algorithm
from A_star import a_star_algorithm
from held_karp import held_karp
from menu import show_start_screen
from table import ResultTable, draw_path
from background import background

# Загрузка изображений
start_img = pygame.image.load(START_IMAGE)
dest_img = pygame.image.load(DEST_IMAGE)
city_img = pygame.image.load(CITY_IMAGE)

# Инициализация шрифта
pygame.font.init()
font = pygame.font.SysFont('Arial', 16)
node_font = pygame.font.SysFont('Arial', 16)

# Создание таблицы результатов
result_table = ResultTable()


def draw_graph(screen, nodes, lines_data, start_node=None, end_node=None, is_aco=False):
    screen.fill(BACKGROUND_COLOR)

    # Рисуем деревья на фоне
    background.draw_trees(screen)

    for line in lines_data:
        pygame.draw.line(screen, (0, 0, 0), nodes[line[0]], nodes[line[1]], 1)
    for index, node in enumerate(nodes):
        if node[1] < HEIGHT - TABLE_HEIGHT:
            if index == start_node:
                screen.blit(start_img, (node[0] - start_img.get_width() // 2, node[1] - start_img.get_height() // 2))
            elif index == end_node:
                screen.blit(dest_img, (node[0] - dest_img.get_width() // 2, node[1] - dest_img.get_height() // 2))
            else:
                screen.blit(city_img, (node[0] - city_img.get_width() // 2, node[1] - city_img.get_height() // 2))

            text_surface = node_font.render(str(index), True, (255, 255, 255))
            screen.blit(text_surface, (node[0] + 5, node[1] + city_img.get_height() // 2))

    result_table.draw(screen)
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    graph_type = None
    nodes, lines_data = [], []
    start_node, end_node = None, None

    show_start_screen(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    graph_type = 'dense'
                    nodes, lines_data = create_dense_graph(num_nodes)
                    start_node, end_node = find_farthest_nodes(nodes, min_distance_nodes=5)
                    background.generate_trees()  # Генерация деревьев при перестройке графа
                    draw_graph(screen, nodes, lines_data, start_node, end_node)
                    result_table.clear()
                elif event.key == pygame.K_s:
                    graph_type = 'sparse'
                    nodes, lines_data = create_sparse_graph(num_nodes)
                    start_node, end_node = find_farthest_nodes(nodes, min_distance_nodes=5)
                    background.generate_trees()  # Генерация деревьев при перестройке графа
                    draw_graph(screen, nodes, lines_data, start_node, end_node)
                    result_table.clear()
                elif event.key == pygame.K_1:
                    if nodes and lines_data:
                        best_path, best_distance, best_iteration = aco_algorithm(nodes, lines_data, start_node)
                        print(
                            f"ACO - Best Path: {best_path}, Best Distance: {best_distance}, Found at Iteration: {best_iteration}")
                        draw_path(screen, nodes, best_path, lines_data, best_distance, best_iteration, "ACO", start_img,
                                  dest_img, result_table, [city_img], node_font, start_node, end_node)
                elif event.key == pygame.K_2:
                    if nodes and lines_data:
                        best_path, best_distance, iterations = a_star_algorithm(nodes, lines_data, start_node, end_node)
                        print(f"A* - Best Path: {best_path}, Best Distance: {best_distance}, Iterations: {iterations}")
                        draw_path(screen, nodes, best_path, lines_data, best_distance, iterations, "A*", start_img,
                                  dest_img, result_table, [city_img], node_font, start_node, end_node)
                elif event.key == pygame.K_3:
                    if nodes and lines_data:
                        best_path, best_distance, iterations = held_karp(nodes, lines_data)
                        print(
                            f"Held-Karp - Best Path: {best_path}, Best Distance: {best_distance}, Iterations: {iterations}")
                        draw_path(screen, nodes, best_path, lines_data, best_distance, iterations, "Held-Karp",
                                  start_img, dest_img, result_table, [city_img], node_font, start_node, end_node)
                elif event.key == pygame.K_m:
                    show_start_screen(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
