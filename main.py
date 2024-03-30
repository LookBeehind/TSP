from UI import *
graph = Graphs()

if __name__ == "__main__":
    pygame.init()
    home_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    nodes = graph.generate_random_coordinates(num_nodes)
                    city_numbers = graph.generate_random_cities(nodes)
                    tree_numbers, tree_coords = graph.generate_random_trees()
                    graph.draw_current_cities(screen, nodes, city_numbers, True)
                    graph.draw_current_trees(tree_numbers, tree_coords)
                if event.key == pygame.K_1:
                    graph.draw_shortest_path(1)
                if event.key == pygame.K_2:
                    graph.draw_shortest_path(2)
                if event.key == pygame.K_3:
                    graph.draw_shortest_path(3)

        pygame.display.flip()
        clock.tick(FPS)
