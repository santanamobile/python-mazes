import random
import pygame
import sys

def generate_maze(width, height):
    if width % 2 == 0 or height % 2 == 0:
        raise ValueError("A largura e a altura devem ser números ímpares!")

    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(y + ny) // 2][(x + nx) // 2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def mark_start_end(maze):
    maze[1][1] = 'S'
    for x in range(len(maze[0]) - 2, 0, -1):
        if maze[-2][x] == 0:
            maze[-2][x] = 'E'
            break
    return (1, 1), (len(maze[0]) - 2, len(maze) - 2)

def draw_maze(screen, maze, cell_size, player_pos, visited):
    colors = {
        1: (0, 0, 0),        # Parede (preto)
        0: (255, 255, 255),  # Caminho (branco)
        'E': (255, 0, 0)     # Fim (vermelho)
    }
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = colors[cell] if cell in colors else (255, 255, 255)
            pygame.draw.rect(
                screen,
                color,
                (x * cell_size, y * cell_size, cell_size, cell_size)
            )

    # Desenhar o caminho percorrido
    for pos in visited:
        pygame.draw.rect(
            screen,
            (255, 255, 0),  # Cor amarela
            (pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)
        )

    # Desenhar o jogador
    pygame.draw.rect(
        screen,
        (0, 255, 0),  # Cor verde
        (player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size)
    )

def reset_game():
    width, height = 21, 21
    maze = generate_maze(width, height)
    start, end = mark_start_end(maze)
    return maze, start, end, list(start), []

def main():
    # Configurações iniciais
    cell_size = 20

    pygame.init()
    screen_width, screen_height = 21 * cell_size, 21 * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Labirinto")
    bold_font = pygame.font.Font(pygame.font.get_default_font(), 80)

    # Inicializar o jogo
    maze, start, end, player_pos, visited = reset_game()
    clock = pygame.time.Clock()

    running = True
    game_over = False
    start_moved = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_r:
                    maze, start, end, player_pos, visited = reset_game()
                    game_over = False
                    start_moved = False
                if not game_over:
                    if event.key == pygame.K_UP and maze[player_pos[1] - 1][player_pos[0]] != 1:
                        player_pos[1] -= 1
                        start_moved = True
                    if event.key == pygame.K_DOWN and maze[player_pos[1] + 1][player_pos[0]] != 1:
                        player_pos[1] += 1
                        start_moved = True
                    if event.key == pygame.K_LEFT and maze[player_pos[1]][player_pos[0] - 1] != 1:
                        player_pos[0] -= 1
                        start_moved = True
                    if event.key == pygame.K_RIGHT and maze[player_pos[1]][player_pos[0] + 1] != 1:
                        player_pos[0] += 1
                        start_moved = True

        if start_moved and 'S' in maze[player_pos[1]]:
            maze[start[1]][start[0]] = 0

        if not game_over:
            visited.append(tuple(player_pos))

        screen.fill((0, 0, 0))
        draw_maze(screen, maze, cell_size, player_pos, visited)

        if tuple(player_pos) == end:
            game_over = True
            text = bold_font.render("Fim!", True, (255, 0, 0))  # Amarelo e negrito
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
