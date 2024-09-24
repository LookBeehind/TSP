# menu.py
import pygame
from config import WIDTH, HEIGHT, BACKGROUND_COLOR, GREEN, WHITE


def show_start_screen(screen):
    pygame.font.init()
    title_font = pygame.font.SysFont('Arial', 72)
    menu_font = pygame.font.SysFont('Arial', 36)
    credit_font = pygame.font.SysFont('Arial', 20)

    screen.fill(BACKGROUND_COLOR)

    # Заголовок
    title_surface = title_font.render("TSP", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_surface, title_rect)

    # Меню
    menu_items = ["Press D for Dense Graph", "Press S for Sparse Graph", "Press 1 for ACO", "Press 2 for A*",
                  "Press 3 for Held-Karp", "Press M to open MENU"]
    for i, item in enumerate(menu_items):
        menu_surface = menu_font.render(item, True, WHITE)
        menu_rect = menu_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        screen.blit(menu_surface, menu_rect)

    # Credits
    credits = ["Dicol Oliviu TI-211 F/R", "Gladcov Gleb TI-212 F/R", "Oxani Vadim TI-221 F/R"]
    for i, credit in enumerate(credits):
        credit_surface = credit_font.render(credit, True, WHITE)
        credit_rect = credit_surface.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10 - i * 30))
        screen.blit(credit_surface, credit_rect)

    pygame.display.flip()
    wait_for_key()


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


