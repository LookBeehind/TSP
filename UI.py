from graphs import *


def home_menu():
    font = pygame.font.Font(None, 36)
    menu_text = [
        "[M] Open Menu",
        "[D] Generate a dense graph",
        "[S] Generate a sparse graph",
        "[1] Ant Colony Optimization Algorithm",
        "[2] A* Algorithm",
        "[3] Held-Karp Algorithm",
    ]

    screen.fill(GREEN)

    for i, text in enumerate(menu_text):
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (190, 150 + i * 40))
    pygame.display.flip()
