import pygame
import sys
import os
#Put your own path to aima
sys.path.append(os.getcwd() + "/../aima-python")
print(sys.path)
from search import *

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

last_square = -1, -1
action = None
show_instructions = True
chosen_key_points = False
start = (-1, -1)
end = (-1, -1)

# Cell and board classes
class Cell:
    def __init__(self, status="unvisited"):
        self.status = status

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]

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
cell_size = 30
instruction_area = 60
width, height = 20, 20
screen_width = width * cell_size
screen_height = height * cell_size + instruction_area

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Board Visualization")

# Set up the font
font = pygame.font.Font(None, 24)  # You can adjust the font size and style

# Function to draw the board
def draw_board(board):
    for y, row in enumerate(board.cells):
        for x, cell in enumerate(row):
            color = WHITE
            if cell.status == "wall":
                color = BLACK
            elif cell.status == "start" or cell.status == "end":
                color = ORANGE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, GRAY, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

# Function to get cell coordinates from mouse click
def get_cell_from_click(mouse_pos):
    x, y = mouse_pos
    cell_x = x // cell_size
    cell_y = y // cell_size
    return cell_x, cell_y

# Function to display instructions
def display_instructions():
    text = "Select the start point and end point"
    instruction_surface = font.render(text, True, RED)
    screen.blit(instruction_surface, (10, screen_height - 30))

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
    print("Reset clicked!")
    for y in range(width):
        for x in range(height):
            board.cells[x][y].status = "unvisited"
    last_square = -1, -1
    action = None
    show_instructions = True
    chosen_key_points = False
    start = (-1, -1)
    end = (-1, -1)

# Create a board
board = Board(width, height)

# Create a button
instructionButton = Button("Got it", (screen_width - 125, screen_height - 50), 100, 40, instruction_handle_button_click)
resetButton = Button("Reset", (screen_width - 125, screen_height - 50), 100, 40, reset_grid)


# Variables for tracking drag state
dragging = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
                            board.cells[cell_y][cell_x].status = "start"
                            start = cell_x, cell_y
                            print("Start" + str(start))
                        elif end == (-1, -1):
                            board.cells[cell_y][cell_x].status = "end"
                            end = cell_x, cell_y
                            print("End" + str(end))
                            chosen_key_points = True

                    elif board.cells[cell_y][cell_x].status == "unvisited":
                        board.cells[cell_y][cell_x].status = "wall"
                        action = "wall"
                    elif board.cells[cell_y][cell_x].status == "wall":
                        board.cells[cell_y][cell_x].status = "unvisited"
                        action = "unvisited"
                    last_square = cell_x, cell_y
                elif instructionButton.is_clicked(mouse_pos):
                    instructionButton.command(instructionButton)
                    instructionButton.command = reset_grid
                    show_instructions = False
                elif resetButton.is_clicked(mouse_pos):
                    resetButton.command(resetButton)

        elif event.type == pygame.MOUSEBUTTONUP:
            last_square = -1, -1
            dragging = False
            action = None

    screen.fill(WHITE)
    draw_board(board)
    if show_instructions:
        display_instructions()
        instructionButton.draw(screen, font)
    else:
        resetButton.draw(screen, font)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
