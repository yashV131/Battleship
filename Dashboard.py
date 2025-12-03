#Creates a dashboard
import pygame

# Initialize Pygame nad it's font
pygame.init()
pygame.font.init()

#set the font to Arial, size 24
font = pygame.font.SysFont('Arial', 24)

# Screen dimensions
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battleship Dashboard")

# Predefined Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Player 1's box properties
rect_x1 = 50
rect_y1 = 50
rect_width = 400
rect_height = 400
line_thickness = 5 

# Player 2's box properties
rect_x2 = rect_x1 + rect_width+20

# Grid for battleships
# since this is a 400x400 box, we can fit a 10x10 grid with each cell being 40x40
CELL_SIZE = 20

#draw the grid for battleships
def draw_grid(surface, x0, y0, grid, reveal=False):
    for x in range(20):
        for y in range(20):
            rect = pygame.Rect(x0 + x * CELL_SIZE, y0 + y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            color = (200, 200, 200)
            pygame.draw.rect(surface, color, rect)

# Game loop
running = True
while running:
    # Fill the background
    screen.fill((0,0,0))

    # Draw the boxes for Player 1 and Player 2
    text_surface = font.render('Player 1, place your ships!', True, (255, 255, 255))
    screen.blit(text_surface, (rect_x1, rect_y1-40))   
    draw_grid(screen, rect_x1, rect_y1, {}, reveal=True)
    draw_grid(screen, rect_x2, rect_y1, {}, reveal=True)
    pygame.draw.rect(screen, BLUE, (rect_x1, rect_y1, rect_width, rect_height), line_thickness)
    pygame.draw.rect(screen, BLUE, (rect_x2, rect_y1, rect_width, rect_height), line_thickness)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()