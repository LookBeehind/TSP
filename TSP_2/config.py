import numpy as np
import pygame

# Constants
NODE_RADIUS = 20
WIDTH = 1000
HEIGHT = 800
TABLE_HEIGHT = 200  # Высота области таблицы
GRAPH_HEIGHT = HEIGHT - TABLE_HEIGHT  # Высота области графа
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30

BACKGROUND_COLOR = (0, 153, 76)

# Обновление изображения дерева на изображение города
CITY_IMAGE = 'assets/city1.png'
START_IMAGE = 'assets/start.png'
DEST_IMAGE = 'assets/dest.png'
TREE_IMAGES = [f'assets/tree{i}.png' for i in range(1, 8)]
num_nodes = 10  # Изменено количество узлов

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calculate_total_distance(path, nodes):
    total_distance = sum(euclidean_distance(nodes[path[i]], nodes[path[i + 1]]) for i in range(len(path) - 1))
    total_distance += euclidean_distance(nodes[path[-1]], nodes[path[0]])  # Возврат к начальной точке
    return total_distance

pygame.display.set_caption("IAFPS Project")
