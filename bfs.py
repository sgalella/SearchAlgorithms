import pygame

# Initialize colors in RGB
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize screen size
ROWS = 12
COLS = 12
WIDTH = 20
HEIGHT = WIDTH
MARGIN = 2
size = ((HEIGHT + MARGIN) * COLS + MARGIN, (WIDTH + MARGIN) * ROWS + MARGIN)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breadth-first search (BFS)")

# Initialize grid
grid = [[0 for col in range(COLS)] for row in range(ROWS)]

# Initialize actions in grid
actions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

# Initialize algorithm
visited = []
expanded = []
is_running = False
has_start = False
has_end = False


def get_actions(grid, current_node, actions):
    possible_actions = []
    width = len(grid)
    height = len(grid[0])
    for action in actions.values():
        new_x = current_node[0] + action[0]
        new_y = current_node[1] + action[1]
        if (new_x >= 0 and new_x < height and new_y >= 0 and new_y < width and grid[new_x][new_y] != 'X'):
            possible_actions.append((new_x, new_y))
    return possible_actions


def draw_grid(grid):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 'S':
                pygame.draw.rect(screen, GREEN, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            elif grid[row][col] == 'V':
                pygame.draw.rect(screen, YELLOW, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            elif grid[row][col] == 'E':
                pygame.draw.rect(screen, BLUE, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            elif grid[row][col] == 'G':
                pygame.draw.rect(screen, RED, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            elif grid[row][col] == 'X':
                pygame.draw.rect(screen, BLACK, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            elif grid[row][col] == 'P':
                pygame.draw.rect(screen, WHITE, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))
            else:
                pygame.draw.rect(screen, GRAY, ((WIDTH + MARGIN) * col + MARGIN, (HEIGHT + MARGIN) * row + MARGIN, WIDTH, HEIGHT))


def set_node(grid, node, status):
    if grid[node[0]][node[1]] != 'S' and grid[node[0]][node[1]] != 'G':
        grid[node[0]][node[1]] = status
    return grid


def breadth_first_search(grid, frontier, expanded, visited):
    current_node, path = frontier.pop(0)
    path.append(current_node)
    if (current_node == goal_node):
        for (x, y) in path[1:-1]:
            grid[x][y] = 'P'
        return False
    expanded.append(current_node)
    grid = set_node(grid, current_node, 'E')
    for next_state in get_actions(grid, current_node, actions):
        if next_state not in visited:
            x, y = next_state
            grid = set_node(grid, next_state, 'V')
            visited.append(next_state)
            frontier.append((next_state, path.copy()))
    return True


# Main loop
run = True
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not has_start:
                mousex, mousey = pygame.mouse.get_pos()
                start_node = (mousey // (HEIGHT + MARGIN), mousex // (WIDTH + MARGIN))
                grid[start_node[0]][start_node[1]] = 'S'
                frontier = [(start_node, [])]
                has_start = True
            elif not has_end:
                mousex, mousey = pygame.mouse.get_pos()
                goal_node = (mousey // (HEIGHT + MARGIN), mousex // (WIDTH + MARGIN))
                grid[goal_node[0]][goal_node[1]] = 'G'
                has_end = True
            else:
                mousex, mousey = pygame.mouse.get_pos()
                barrier_node = (mousey // (HEIGHT + MARGIN), mousex // (WIDTH + MARGIN))
                grid[barrier_node[0]][barrier_node[1]] = 'X'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and has_start and has_end:
                is_running = True
    screen.fill(BLACK)
    if is_running:
        is_running = breadth_first_search(grid, frontier, expanded, visited)
    draw_grid(grid)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
