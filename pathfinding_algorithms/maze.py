import pygame


class MazeWindow:
    """ Visualization of maze pathfinder. """
    def __init__(self, rows=12, columns=12, width=20, margin=2, cost=1, title="Maze"):
        """
        Initializes maze visualization.

        Args:
            rows (int, optional): Number of rows of the maze. Defaults to 12.
            columns (int, optional): Number of columns of the maze. Defaults to 12.
            width (int, optional): Width size of each cell. Defaults to 20.
            margin (int, optional): Margin size of each cell. Defaults to 2.
            cost (int, optional): Cost of moving from one cell to another adjacent. Defaults to 1.
            title (str, optional): Title of the Pygame window. Defaults to "Maze".
        """
        # Set window dimensions
        self.rows = int(rows)
        self.columns = int(columns)
        self.width = int(width)
        self.height = self.width
        self.margin = int(margin)
        self.cost = int(cost)
        self.title = title
        self.size = ((self.height + self.margin) * self.columns, (self.width + self.margin) * self.rows + self.margin)

        # Initialize states
        self.state_start = 'S'
        self.state_visited = 'V'
        self.state_explored = 'E'
        self.state_goal = 'G'
        self.state_blocked = 'X'
        self.state_path = 'P'

        # Initialize colors
        self.color_start = (0, 255, 0)
        self.color_visited = (255, 255, 0)
        self.color_explored = (0, 0, 255)
        self.color_goal = (255, 0, 0)
        self.color_blocked = (0, 0, 0)
        self.color_path = (255, 255, 255)
        self.color_default = (112, 128, 144)

        # Initialize grid
        self.grid = [['0' for col in range(self.columns)] for row in range(self.rows)]

        # Load icon
        self.icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(self.icon)

    def draw_grid(self):
        """ Draws maze grid. """
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col] == self.state_start:
                    pygame.draw.rect(self.screen, self.color_start, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))
                elif self.grid[row][col] == self.state_visited:
                    pygame.draw.rect(self.screen, self.color_visited, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))
                elif self.grid[row][col] == self.state_explored:
                    pygame.draw.rect(self.screen, self.color_explored, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))
                elif self.grid[row][col] == self.state_goal:
                    pygame.draw.rect(self.screen, self.color_goal, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))
                elif self.grid[row][col] == self.state_blocked:
                    pygame.draw.rect(self.screen, self.color_blocked, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))
                elif self.grid[row][col] == self.state_path:
                    pygame.draw.rect(self.screen, self.color_path, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))
                else:
                    pygame.draw.rect(self.screen, self.color_default, ((self.width + self.margin) * col + self.margin, (self.height + self.margin) * row + self.margin, self.width, self.height))

    def check_position(self, state):
        """ Checks locations where state occurs. """
        position = []
        for row in range(self.rows):
            for col in range(self.columns):
                if (self.grid[row][col] == state):
                    if state == self.state_start or state == self.state_goal:
                        return (row, col)
                    position.append((row, col))
        return position

    def load(self, name):
        """ Loads grid from file. """
        with open(name, 'r') as file:
            self.grid = [line.strip().split(',') for line in file]

        # Redefine grid properties
        self.rows = len(self.grid)
        self.columns = len(self.grid[0])
        self.size = ((self.height + self.margin) * self.columns, (self.width + self.margin) * self.rows + self.margin)

    def save(self, name):
        """ Saves maze as text file with filename name. """
        # Check position of start, goal and blocked nodes
        start_node = self.check_position(self.state_start)
        goal_node = self.check_position(self.state_goal)
        blocked_nodes = self.check_position(self.state_blocked)

        # Create new maze
        new_maze = [['0' for col in range(self.columns)] for row in range(self.rows)]
        new_maze[start_node[0]][start_node[1]] = self.state_start
        new_maze[goal_node[0]][goal_node[1]] = self.state_goal
        for blocked_node in blocked_nodes:
            new_maze[blocked_node[0]][blocked_node[1]] = self.state_blocked

        # Save file
        with open(name, 'w') as file:
            for row in new_maze:
                for idx, col in enumerate(row):
                    if idx == 0:
                        file.write(col)
                    else:
                        file.write("," + col)
                file.write("\n")

    def run(self, is_expansion, algorithm):
        """
        Runs the pathfinder algorithm.

        Args:
            is_expansion (bool): Node expansion is visible or not.
            algorithm ([type]): Algorithm to solve the maze.
        """
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

        # Initialize algorithm
        if algorithm == "Breadth-first search (BFS)":
            solve_maze = self.breadth_first_search
            self.cost_grid = self.calculate_cost_grid(None)
        elif algorithm == "Depth-first search (DFS)":
            solve_maze = self.depth_first_search
            self.cost_grid = self.calculate_cost_grid(None)
        elif algorithm == "Dijkstra's algorithm":
            solve_maze = self.dijkstra
            self.cost_grid = self.calculate_cost_grid("cost")
        elif algorithm == "Greedy best-first search (GBFS)":
            solve_maze = self.greedy_best_first_search
            self.cost_grid = self.calculate_cost_grid("heuristic")
        elif algorithm == "A*":
            solve_maze = self.a_star
            self.cost_grid = self.calculate_cost_grid("cost+heuristic")

        # Initialize nodes
        self.start_node = self.check_position(self.state_start)
        self.goal_node = self.check_position(self.state_goal)
        self.open_nodes = [(self.start_node, self.get_cost_node(self.cost_grid, self.start_node))]
        self.closed_nodes = []
        self.best_path = {}

        # Initialize actions
        self.actions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

        # Save maze copy
        self.grid_backup = [row.copy() for row in self.grid]

        # Run loop
        self.clock = pygame.time.Clock()
        is_running = True
        is_maze_solved = False

        # Maze loop
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            if not is_maze_solved:
                if is_expansion:
                    while True:
                        is_maze_solved = solve_maze()
                        self.clear_maze()
                        if is_maze_solved:
                            for (x, y) in self.full_path[:-1]:
                                self.grid[x][y] = self.state_path
                            break
                else:
                    is_maze_solved = solve_maze()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()
        self.clear_maze()

    def set_node(self, node, state):
        """ Sets node to be at a given state. """
        if self.grid[node[0]][node[1]] != self.state_start and self.grid[node[0]][node[1]] != self.state_goal:
            self.grid[node[0]][node[1]] = state

    def generate_path(self, current_node):
        """ Generates optimal path from goal to beginning. """
        self.full_path = []
        while current_node in self.best_path.keys():
            current_node = self.best_path[current_node]
            self.full_path.append(current_node)

    def calculate_cost_grid(self, method):
        """ Calculates cost at position using a given method. """
        goal_node = self.check_position(self.state_goal)
        total_cost = []
        if method == "cost":
            total_cost = [[self.cost for col in range(self.columns)] for row in range(self.rows)]
        elif method == "heuristic":
            total_cost = [[abs(goal_node[0] - row) + abs(goal_node[1] - col) for col in range(self.columns)] for row in range(self.rows)]
        elif method == "cost+heuristic":
            total_cost = [[abs(goal_node[0] - row) + abs(goal_node[1] - col) + self.cost for col in range(self.columns)] for row in range(self.rows)]
        else:
            total_cost = [[0 for col in range(self.columns)] for row in range(self.rows)]

        return total_cost

    def get_cost_node(self, cost_grid, node):
        """ Gets cost of a given node. """
        return cost_grid[node[0]][node[1]]

    def get_actions(self, current_node):
        """ Gets available actions of a given node. """
        possible_actions = []
        for action in self.actions.values():
            new_x = current_node[0] + action[0]
            new_y = current_node[1] + action[1]
            if (new_x >= 0 and new_x < self.rows and new_y >= 0 and new_y < self.columns and self.grid[new_x][new_y] != self.state_blocked):
                possible_actions.append((new_x, new_y))
        return possible_actions

    def clear_maze(self):
        """ Resets maze grid. """
        self.grid = [row.copy() for row in self.grid_backup]

    def a_star(self):
        """ Runs the A* algorithm. """  # TODO: Move algorithms to module algorithms.py
        current_node, _ = self.open_nodes.pop(0)
        if (current_node == self.goal_node):
            self.generate_path(current_node)
            for (x, y) in self.full_path[:-1]:
                self.grid[x][y] = self.state_path
            return True
        self.closed_nodes.append(current_node)
        self.set_node(current_node, self.state_explored)
        for next_state in self.get_actions(current_node):
            next_cost = self.get_cost_node(self.cost_grid, next_state)
            if (next_state, next_cost) not in self.open_nodes and next_state not in self.closed_nodes:
                self.best_path[next_state] = current_node
                self.set_node(next_state, self.state_visited)
                self.open_nodes.append((next_state, next_cost))
        self.open_nodes.sort(key=lambda x: x[1])
        return False

    def breadth_first_search(self):
        """ Runs the BFS algorithm. """
        current_node, _ = self.open_nodes.pop(0)
        if (current_node == self.goal_node):
            self.generate_path(current_node)
            for (x, y) in self.full_path[:-1]:
                self.grid[x][y] = self.state_path
            return True
        self.closed_nodes.append(current_node)
        self.set_node(current_node, self.state_explored)
        for next_state in self.get_actions(current_node):
            if (next_state, 0) not in self.open_nodes and next_state not in self.closed_nodes:
                self.best_path[next_state] = current_node
                self.set_node(next_state, self.state_visited)
                self.open_nodes.append((next_state, 0))
        return False

    def depth_first_search(self):
        """ Runs the DFS algorithm. """ 
        current_node, _ = self.open_nodes.pop(-1)
        if (current_node == self.goal_node):
            self.generate_path(current_node)
            for (x, y) in self.full_path[:-1]:
                self.grid[x][y] = self.state_path
            return True
        self.closed_nodes.append(current_node)
        self.set_node(current_node, self.state_explored)
        for next_state in self.get_actions(current_node):
            if (next_state, 0) not in self.open_nodes and next_state not in self.closed_nodes:
                self.best_path[next_state] = current_node
                self.set_node(next_state, self.state_visited)
                self.open_nodes.append((next_state, 0))
        return False

    def dijkstra(self):
        """ Runs the Dijkstra algorithm. """
        current_node, _ = self.open_nodes.pop(0)
        if (current_node == self.goal_node):
            self.generate_path(current_node)
            for (x, y) in self.full_path[:-1]:
                self.grid[x][y] = self.state_path
            return True
        self.closed_nodes.append(current_node)
        self.set_node(current_node, self.state_explored)
        for next_state in self.get_actions(current_node):
            next_cost = self.get_cost_node(self.cost_grid, next_state)
            if (next_state, next_cost) not in self.open_nodes and next_state not in self.closed_nodes:
                self.best_path[next_state] = current_node
                self.set_node(next_state, self.state_visited)
                self.open_nodes.append((next_state, next_cost))
        self.open_nodes.sort(key=lambda x: x[1])
        return False

    def greedy_best_first_search(self):
        """ Runs the GBFS algorithm. """
        current_node, _ = self.open_nodes.pop(0)
        if (current_node == self.goal_node):
            self.generate_path(current_node)
            for (x, y) in self.full_path[:-1]:
                self.grid[x][y] = self.state_path
            return True
        self.closed_nodes.append(current_node)
        self.set_node(current_node, self.state_explored)
        for next_state in self.get_actions(current_node):
            next_cost = self.get_cost_node(self.cost_grid, next_state)
            if (next_state, next_cost) not in self.open_nodes and next_state not in self.closed_nodes:
                self.best_path[next_state] = current_node
                self.set_node(next_state, self.state_visited)
                self.open_nodes.append((next_state, next_cost))
        self.open_nodes.sort(key=lambda x: x[1])
        return False

    def edit(self):
        """ Edits the maze. """
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

        has_start = any([self.state_start in row for row in self.grid])
        has_goal = any([self.state_goal in row for row in self.grid])

        # Run loop
        is_running = True
        self.clock = pygame.time.Clock()
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not has_start:
                    mousex, mousey = pygame.mouse.get_pos()
                    start_node = (mousey // (self.height + self.margin), mousex // (self.width + self.margin))
                    if self.grid[start_node[0]][start_node[1]] != self.state_goal:
                        self.grid[start_node[0]][start_node[1]] = self.state_start
                        has_start = True
                elif not has_goal:
                    mousex, mousey = pygame.mouse.get_pos()
                    goal_node = (mousey // (self.height + self.margin), mousex // (self.width + self.margin))
                    if self.grid[goal_node[0]][goal_node[1]] != self.state_start:
                        self.grid[goal_node[0]][goal_node[1]] = self.state_goal
                        has_goal = True
                else:
                    if has_start and has_goal:
                        mousex, mousey = pygame.mouse.get_pos()
                        barrier_node = (mousey // (self.height + self.margin), mousex // (self.width + self.margin))
                        if self.grid[barrier_node[0]][barrier_node[1]] == self.state_blocked:
                            self.grid[barrier_node[0]][barrier_node[1]] = 0
                        elif self.grid[barrier_node[0]][barrier_node[1]] == self.state_start and has_goal:
                            self.grid[barrier_node[0]][barrier_node[1]] = 0
                            has_start = False
                        elif self.grid[barrier_node[0]][barrier_node[1]] == self.state_goal and has_start:
                            self.grid[barrier_node[0]][barrier_node[1]] = 0
                            has_goal = False
                        elif self.grid[barrier_node[0]][barrier_node[1]] != self.state_start and self.grid[barrier_node[0]][barrier_node[1]] != self.state_start:
                            self.grid[barrier_node[0]][barrier_node[1]] = self.state_blocked
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()
