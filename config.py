import pygame
import sys
import random
import math
import numpy as np
import itertools
import heapq

# Constants
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (66, 245, 161)
GRAY = (149, 163, 186)

# Algorithm variables
num_nodes = 10
gens = 1000
mut_rate = 0.1
pop_size = 50

# Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IAFPS Project")
win_icon = pygame.image.load("assets/algorithm.png")
pygame.display.set_icon(win_icon)
clock = pygame.time.Clock()
