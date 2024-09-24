import pygame
import random
from config import WIDTH, HEIGHT, GRAPH_HEIGHT, TREE_IMAGES

class Background:
    def __init__(self, num_trees=30):
        self.num_trees = num_trees
        self.tree_positions = []
        self.tree_images = [pygame.image.load(tree_img) for tree_img in TREE_IMAGES]
        self.current_trees = []

    def generate_trees(self):
        self.tree_positions = []
        for _ in range(self.num_trees):
            x = random.randint(0, WIDTH)
            y = random.randint(0, GRAPH_HEIGHT)
            self.tree_positions.append((x, y))

    def draw_trees(self, screen):
        if len(self.current_trees) == 0:
            for _ in self.tree_positions:
                tree_img = random.choice(self.tree_images)
                self.current_trees.append(tree_img)

        for pos, tree in zip(self.tree_positions, self.current_trees):
            screen.blit(tree, (pos[0] - tree.get_width() // 2, pos[1] - tree.get_height() // 2))


# Initialize background
background = Background()
