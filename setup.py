import pygame
from datetime import datetime
from datetime import timedelta
import time
import sys
import os
import math
import random
#Put your own path to aima
sys.path.append(os.getcwd() + "/../aima-python")
print(sys.path)
from search import *

# Definitions
# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Define statuses
UNVISITED = 0
VISITED = 1
WALL = 2
START = 100
END = 101
PATH = 102

# Define Algorithms
ASTAR = 0
BREADTH_FIRST_SEARCH = 1
DEPTH_FIRST_SEARCH = 2
DIJKSTRA = 3
ITERATIVE_DEEPENING_ASTAR = 4
GREEDY = 5

# Define Heuristics
MANHATTAN = 0
EUCLIDEAN = 1
CHEBYSHEV = 2
ABS_DIFFERENCE = 3
# End of Defintions

# Global Variables
last_square = -1, -1
action = None
show_instructions = True
chosen_key_points = False
start = (-1, -1)
end = (-1, -1)
current_cell = (-1, -1)
current_search_algorithm = 0

solution_shown = False
full_path = []
update_board = True
# End of Global Variables

# Class Definitions
class GridProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def actions(self, state):
        x, y = state  # Current cell coordinates

        # Define possible moves: (dx, dy)
        moves = [
            (0, -1),  # Move up
            (0, 1),   # Move down
            (-1, 0),  # Move left
            (1, 0),   # Move right
            (1, -1),  # Move up - right
            (-1, -1), # Move up - left
            (1, 1),   # Move down - right
            (-1, 1)   # Move down - left
        ]

        # Check if each move is valid and within the bounds of the grid
        valid_moves = [
            (x + dx, y + dy)
            for dx, dy in moves
            if 0 <= x + dx < width and 0 <= y + dy < height
            and board.cells[y + dy][x + dx].status != WALL
        ]
        return valid_moves
    
    def result(self, state, action):
        # The action is the new cell coordinates after the move
        x, y = action
        full_path.append((x, y, datetime.now()))
        return action
    
    def goal_test(self, state):
        # Implement the goal test
        return state == self.goal
    
    def h(self, node):
        # Manhattan distance heuristic
        (x1, y1) = node.state
        (x2, y2) = self.goal
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        # Heuristics under
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy) # Manhattan
        return max(abs(x1 - y1), abs(x2 - y2)) # Chebyshev
        return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) # Euclidean
        return abs(x1 - y1) + abs(x2 - y2) # Abs Diff

class Cell:
    def __init__(self, status=UNVISITED):
        self.status = status
        self.time_visited = None

    def __str__(self) -> str:
        retVal = '['
        
        match self.status:
            case 0: # UNVISITED
                retVal += ' '
            case 1: # VISITED
                retVal += '-'
            case 2: # WALL
                retVal += 'X'
            case 100:
                retVal += 'S'
            case 101:
                retVal += 'E'
            case 102:
                retVal += 'P'
        retVal += ']'
        return retVal

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
    
    def __str__(self) -> str:
        retVal = ""
        for y in range(self.height):
            for x in range(self.width):
                retVal += str(self.cells[y][x])
            retVal += '\n'
        return retVal
    
    def get_state(self):
        # Convert the board state to a tuple
        return tuple(tuple(cell.status for cell in row) for row in self.cells)

    def update_from_solution(self, solution):
        # Extract the sequence of actions from the solution
        actions = solution.solution()

        # Update the board state based on the actions
        # last_time = full_path[0][2]
        for data in full_path:
            x, y, timestamp = data
            if (x, y) != start or (x, y) != end:
                color = GRAY
                pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, GRAY, (x * cell_size, y * cell_size, cell_size, cell_size), 1)
                pygame.display.flip()
                pygame.time.Clock().tick(240)
                # time.sleep((timestamp - last_time).total_seconds())
                # last_time = timestamp
        for i in range(len(actions)):
            # Assuming action is a tuple (x, y) representing the cell coordinates
            x1, y1 = actions[i]
            if (x1, y1) != start or (x1, y1) != END:
                self.cells[y1][x1].status = PATH
                color = BLUE
                pygame.draw.rect(screen, color, (x1 * cell_size, y1 * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, GRAY, (x1 * cell_size, y1 * cell_size, cell_size, cell_size), 1)

                pygame.display.flip()
                pygame.time.Clock().tick(240)
                time.sleep(0.005)  # Adjust this value to control the speed of the line drawing
        x1, y1 = start
        x2, y2 = actions[0]
        pygame.draw.line(screen, RED, (x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2),
                        (x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2), 2)
        for i in range(len(actions) - 1):
            x1, y1 = actions[i]
            x2, y2 = actions[i + 1]
            pygame.draw.line(screen, RED, (x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2),
                        (x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2), 2)
        pygame.draw.rect(screen, ORANGE, (start[0] * cell_size, start[1] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, GRAY, (start[0] * cell_size, start[1] * cell_size, cell_size, cell_size), 1)
        pygame.draw.rect(screen, ORANGE, (end[0] * cell_size, end[1] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, GRAY, (end[0] * cell_size, end[1] * cell_size, cell_size, cell_size), 1)
        pygame.display.flip()
        pygame.time.Clock().tick(240)

# Button class
class Button:
    def __init__(self, text, position, width, height, command):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.command = command

    def draw(self, surface, font):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Initialize Pygame
pygame.init()

# Set up the display
cell_size = 10
instruction_area = 340
width, height = 80, 40
screen_width = width * cell_size
screen_height = height * cell_size + instruction_area

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Board Visualization")

# Set up the font
font = pygame.font.Font(None, 24)  # You can adjust the font size and style

# Function to draw the board
def draw_board(board):
    now = datetime.now()
    for y, row in enumerate(board.cells):
        for x, cell in enumerate(row):
            color = WHITE
            if cell.status == WALL:
                color = BLACK
            elif cell.status == START or cell.status == END:
                color = ORANGE
            elif cell.status == VISITED:
                delta = now - cell.time_visited
                if delta.total_seconds() >= 1:
                    color = GRAY
                else:
                    gradient = GRAY[0] + 0.000155 * (1000000 - delta.microseconds)
                    color = gradient, gradient, gradient
            elif cell.status == PATH:
                color = BLUE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, GRAY, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

# Function to get cell coordinates from mouse click
def get_cell_from_click(mouse_pos):
    x, y = mouse_pos
    cell_x = x // cell_size
    cell_y = y // cell_size
    return cell_x, cell_y

# Function to handle button click
def instruction_handle_button_click(button):
    # Add logic to handle button click
    print("Button clicked!")
    # You can update your logic here to get rid of the instruction text

def reset_grid(button):
    global last_square
    global action
    global show_instructions
    global chosen_key_points
    global start
    global end
    global current_cell
    global solution_shown
    global full_path
    global update_board
    print("Reset clicked!")
    for y in range(width):
        for x in range(height):
            board.cells[x][y].status = UNVISITED
    last_square = -1, -1
    action = None
    show_instructions = True
    chosen_key_points = False  # Set chosen_key_points to False
    start = (-1, -1)
    end = (-1, -1)
    current_cell = (-1, -1)
    solution_shown = False
    full_path = []
    update_board = True
    for i in range(1500):
        cell_y = random.randint(0,height - 1)
        cell_x = random.randint(0,width - 1)
        while board.cells[cell_y][cell_x].status == WALL:
            cell_y = random.randint(0,height - 1)
            cell_x = random.randint(0,width - 1)
        board.cells[cell_y][cell_x].status = WALL

def clear_grid(button):
    global last_square
    global action
    global show_instructions
    global chosen_key_points
    global start
    global end
    global current_cell
    global solution_shown
    global full_path
    global update_board
    print("Clear clicked!")
    for y in range(width):
        for x in range(height):
            board.cells[x][y].status = UNVISITED
    last_square = -1, -1
    action = None
    show_instructions = True
    chosen_key_points = False  # Set chosen_key_points to False
    start = (-1, -1)
    end = (-1, -1)
    current_cell = (-1, -1)
    solution_shown = False
    full_path = []
    update_board = True

def configure_buttons():
    # TODO
    pass

def search(problem):
    match current_search_algorithm:
        case 0:
            t0 = time.time()
            solution = astar_search(problem)
            t1 = time.time()
        case 1:
            t0 = time.time()
            solution = breadth_first_tree_search(problem)
            t1 = time.time()
        case 2:
            t0 = time.time()
            solution = depth_first_tree_search(problem)
            t1 = time.time()
        case 3:
            t0 = time.time()
            solution = best_first_graph_search(problem, lambda node: node.path_cost)
            t1 = time.time()
        case 4:
            t0 = time.time()
            solution = iterative_deepening_search(problem)
            t1 = time.time()
        case 5:
            t0 = time.time()
            solution = best_first_graph_search(problem, lambda node: node.path_cost)
            t1 = time.time()
    return t0, t1, solution


# Create a board
board = Board(width, height)

# Create a button
readyButton = Button("Ready", (screen_width - 125, screen_height - 320), 100, 40, instruction_handle_button_click)
resetButton = Button("Reset", (screen_width - 250, screen_height - 320), 100, 40, reset_grid)
cleanBoardButton = Button("Clear Board", (screen_width - 250, screen_height - 270), 100, 40, clear_grid)

# Create algorithm buttons
astarButton = Button("Astar Search", (25, screen_height - 320), 100, 40, configure_buttons)
breadthButton = Button("BFS Search", (25, screen_height - 270), 100, 40, configure_buttons)
depthButton = Button("DFS Search", (25, screen_height - 220), 100, 40, configure_buttons)
dijkstraButton = Button("Dijkstra Search", (25, screen_height - 170), 100, 40, configure_buttons)
IDAButton = Button("IDA Search", (25, screen_height - 120), 100, 40, configure_buttons)
greedyButton = Button("Greedy Search", (25, screen_height - 70), 100, 40, configure_buttons)



# Variables for tracking drag state
dragging = False
print((height, width))
for i in range(1500):
    cell_y = random.randint(0,height - 1)
    cell_x = random.randint(0,width - 1)
    print((cell_x, cell_y))
    while board.cells[cell_y][cell_x].status == WALL:
        cell_y = random.randint(0,height - 1)
        cell_x = random.randint(0,width - 1)
    board.cells[cell_y][cell_x].status = WALL

# Main game loop
while True:
    now = datetime.now()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if chosen_key_points:
                if event.key == pygame.K_UP:
                    # Move up
                    new_y = max(current_cell[1] - 1, 0)
                    if board.cells[new_y][current_cell[0]].status != WALL:
                        if board.cells[new_y][current_cell[0]].status == UNVISITED:
                            board.cells[new_y][current_cell[0]].status = VISITED
                            board.cells[new_y][current_cell[0]].time_visited = now
                        current_cell = current_cell[0], new_y

                elif event.key == pygame.K_DOWN:
                    # Move down
                    new_y = min(current_cell[1] + 1, height - 1)
                    if board.cells[new_y][current_cell[0]].status != WALL:
                        if board.cells[new_y][current_cell[0]].status == UNVISITED:
                            board.cells[new_y][current_cell[0]].status = VISITED
                            board.cells[new_y][current_cell[0]].time_visited = now
                        current_cell = current_cell[0], new_y

                elif event.key == pygame.K_LEFT:
                    # Move left
                    new_x = max(current_cell[0] - 1, 0)
                    if board.cells[current_cell[1]][new_x].status != WALL:
                        if board.cells[current_cell[1]][new_x].status == UNVISITED:
                            board.cells[current_cell[1]][new_x].status = VISITED
                            board.cells[current_cell[1]][new_x].time_visited = now
                        current_cell = new_x, current_cell[1]

                elif event.key == pygame.K_RIGHT:
                    # Move right
                    new_x = min(current_cell[0] + 1, width - 1)
                    if board.cells[current_cell[1]][new_x].status != WALL:
                        if board.cells[current_cell[1]][new_x].status == UNVISITED:
                            board.cells[current_cell[1]][new_x].status = VISITED
                            board.cells[current_cell[1]][new_x].time_visited = now
                        current_cell = new_x, current_cell[1]
                        
        elif event.type == pygame.MOUSEMOTION and dragging and chosen_key_points:
            mouse_pos = pygame.mouse.get_pos()
            cell_x, cell_y = get_cell_from_click(mouse_pos)
            # Toggle the status of the cell while dragging
            if 0 <= cell_x < width and 0 <= cell_y < height and start != (cell_x, cell_y) and end != (cell_x, cell_y):
                board.cells[cell_y][cell_x].status = action

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                cell_x, cell_y = get_cell_from_click(mouse_pos)
                dragging = True
                # Toggle the status of the clicked cell
                if 0 <= cell_x < width and 0 <= cell_y < height:
                    if chosen_key_points == False:
                        if start == (-1, -1):
                            board.cells[cell_y][cell_x].status = START
                            start = cell_x, cell_y
                            current_cell = cell_x, cell_y
                        elif end == (-1, -1):
                            board.cells[cell_y][cell_x].status = END
                            end = cell_x, cell_y
                            chosen_key_points = True

                    elif board.cells[cell_y][cell_x].status == UNVISITED:
                        board.cells[cell_y][cell_x].status = WALL
                        action = WALL
                    elif board.cells[cell_y][cell_x].status == WALL:
                        board.cells[cell_y][cell_x].status = UNVISITED
                        action = UNVISITED
                    last_square = cell_x, cell_y

                elif readyButton.is_clicked(mouse_pos):
                    readyButton.command(readyButton)
                    show_instructions = False

                elif resetButton.is_clicked(mouse_pos):
                    resetButton.command(resetButton)

                elif cleanBoardButton.is_clicked(mouse_pos):
                    cleanBoardButton.command(cleanBoardButton)
                # Here
# ASTAR = 0
# BREADTH_FIRST_SEARCH = 1
# DEPTH_FIRST_SEARCH = 2
# DIJKSTRA = 3
# ITERATIVE_DEEPENING_ASTAR = 4
# GREEDY = 5
                elif astarButton.is_clicked(mouse_pos):
                    current_search_algorithm = ASTAR
                    astarButton.command()
                
                elif breadthButton.is_clicked(mouse_pos):
                    current_search_algorithm = BREADTH_FIRST_SEARCH
                    breadthButton.command()
                
                elif depthButton.is_clicked(mouse_pos):
                    current_search_algorithm = DEPTH_FIRST_SEARCH
                    depthButton.command()
                
                elif dijkstraButton.is_clicked(mouse_pos):
                    current_search_algorithm = DIJKSTRA
                    dijkstraButton.command()
                
                elif IDAButton.is_clicked(mouse_pos):
                    current_search_algorithm = ITERATIVE_DEEPENING_ASTAR
                    IDAButton.command()

                elif greedyButton.is_clicked(mouse_pos):
                    current_search_algorithm = GREEDY
                    greedyButton.command()

        elif event.type == pygame.MOUSEBUTTONUP:
            last_square = -1, -1
            dragging = False
            action = None

    if chosen_key_points and show_instructions == False and solution_shown == False:
        # Create a GridProblem instance
        problem = GridProblem(start, end)

        # Solve
        t0, t1, solution = search(problem)

        # Update the board based on the solution
        if solution:
            print(start)
            for action in solution.solution():
                x, y = action
                if board.cells[y][x].status == UNVISITED:
                    print("UNVISITED")
                    board.cells[y][x].status = PATH
                    board.cells[y][x].time_visited = now
                    if (x, y) == end:
                        break
                    else:
                        print((x, y))
                elif board.cells[y][x].status == END:
                    print("END")
                    for pathCord in full_path:
                        if board.cells[pathCord[1]][pathCord[0]].status == UNVISITED:
                            board.cells[pathCord[1]][pathCord[0]].status = VISITED
                        board.cells[pathCord[1]][pathCord[0]].time_visited = pathCord[2]
                    board.cells[y][x].status = END
                    board.cells[y][x].time_visited = now
                    solution_shown = True
                    break
                else:
                    board.cells[y][x].time_visited = now
                    print(board.cells[y][x].status)
                current_cell = x, y  # Update current_cell

            # Update the board based on the solution
            board.update_from_solution(solution)
            update_board = False
            print(t1-t0)
        else:
            reset_grid(resetButton)
    # if current_cell == end:
    #     reset_grid(resetButton)
    if update_board:
        screen.fill(WHITE)
        draw_board(board)
    if show_instructions:
        readyButton.draw(screen, font)
    else:
        resetButton.draw(screen, font)
        cleanBoardButton.draw(screen, font)
        astarButton.draw(screen, font)
        breadthButton.draw(screen, font)
        depthButton.draw(screen, font)
        dijkstraButton.draw(screen, font)
        IDAButton.draw(screen, font)
        greedyButton.draw(screen, font)

    pygame.display.flip()
    pygame.time.Clock().tick(60)