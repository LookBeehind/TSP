from UI import *
graph = Graphs()

if __name__ == "__main__":
    pygame.init()
    home_menu()
    show_lines = True
    while True:
        for event in pygame.event.get():
            nodes = graph.generate_random_coordinates(num_nodes)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    graph.draw_graph(screen, nodes, show_lines)
                if event.key == pygame.K_1:
                    graph.draw_shortest_path(1)
                if event.key == pygame.K_2:
                    graph.draw_shortest_path(2)
                if event.key == pygame.K_3:
                    graph.draw_shortest_path(3)

        pygame.display.flip()
        clock.tick(FPS)
