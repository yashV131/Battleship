#REQUIREMENTS:
'''
• Display the rules of the game and instructions for the user
• Display a set of options for the various things your players can do (display instructions,
display score, quit early, etc)
• Utilize basic coding elements taught in this class including if-elif-else statements, loops,
dictionaries, functions (with docstrings), try-except statements, and comments
• Use file input/output for something
• Create a nice-looking user interface (consider using turtle graphics, tkinter, or pygame)
• Create a complete, fully functional, high quality gaming experience
• Incorporate at least one thing beyond what is covered in the course (learn something
new)
• Be creative and have fun!
Use only 1 class! Multiple classes cannot be created.
'''
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

# Initialize for mouse position
mouse_x, mouse_y = None, None

#reveal grids toggle
reveal1 = True
#Initialize plater grids: (x,y):False (no ship) or True (ship)
player1_grid = {(x, y): False for x in range(20) for y in range(20)}
player2_grid = {(x, y): False for x in range(20) for y in range(20)}

player1_clicks = []
player2_clicks = []

#draw the grid for battleships
def draw_grid(surface, x0, y0, grid,reveal=False,player_name=''):
    if(reveal):
        for x in range(20):
            for y in range(20):
                # calculate cell position
                leftwall = x0 + x * CELL_SIZE
                topwall = y0 + y * CELL_SIZE
                rightwall = leftwall + CELL_SIZE-1
                bottomwall = topwall + CELL_SIZE-1

                #draw original grid
                rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                color = WHITE
                pygame.draw.rect(surface, color, rect)
                for x_coord,y_coord in player1_clicks:
                    if x_coord is not None and y_coord is not None:
                        #check if mouse is inside the cell
                        if leftwall <= x_coord <= rightwall and topwall <= y_coord <= bottomwall:
                            #draw black box
                            # rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                            pygame.draw.rect(surface, RED, rect)
                for x_coord,y_coord in player2_clicks:
                    if x_coord is not None and y_coord is not None:
                        #check if mouse is inside the cell
                        if leftwall <= x_coord <= rightwall and topwall <= y_coord <= bottomwall:
                            #draw black box
                            # rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                            pygame.draw.rect(surface, RED, rect)
                
    else:
        rect = pygame.Rect(x0, y0, CELL_SIZE*20-1, CELL_SIZE*20-1)
        color = (0,0,0)
        pygame.draw.rect(surface, color, rect)
        text_surface = font.render('It is not your turn yet!', True, (255, 255, 255))
        screen.blit(text_surface, (x0+100, y0+190))
  
def reveal_player_ships(reveal1):
    if(reveal1):
        # Player 1's turn
        text_surface = font.render('Player 1, place your ships!', True, (255, 255, 255))
        screen.blit(text_surface, (rect_x1, rect_y1-40))  
        
        draw_grid(screen, rect_x1, rect_y1, {},reveal1,"player1")
        draw_grid(screen, rect_x2, rect_y1, {})
    else:
        # Player 2's turn
        text_surface = font.render('Player 2, place your ships!', True, (255, 255, 255))
        screen.blit(text_surface, (rect_x2, rect_y1-40))  
        
        draw_grid(screen, rect_x1, rect_y1, {})
        draw_grid(screen, rect_x2, rect_y1, {},True,"player2") 
   

# def event_handler():
#      #Display mouse coordinates    
#     global mouse_x, mouse_y
#     x_coord, y_coord = pygame.mouse.get_pos()
#     mouse_text = font.render(f' X,Y:({x_coord}, {y_coord})', True, WHITE)
#     screen.blit(mouse_text, (800,500))
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             return False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_x, mouse_y = pygame.mouse.get_pos()
            
#             player1_clicks.append((mouse_x, mouse_y))
#             #draw grid with black box
#             draw_grid(screen, rect_x1, rect_y1, {},reveal1)
#             print(f'Mouse clicked at: ({mouse_x}, {mouse_y})')
#     return True

def event_handler():
    global mouse_x, mouse_y, reveal1

    # Display mouse coordinates    
    x_coord, y_coord = pygame.mouse.get_pos()
    mouse_text = font.render(f' X,Y:({x_coord}, {y_coord})', True, WHITE)
    screen.blit(mouse_text, (800, 500))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if len(player2_clicks) >= 5:
                print("Both players have finished placing ships.")
                
            # PLAYER 1 TURN
            elif reveal1:
                player1_clicks.append((mouse_x, mouse_y))
                print("P1 click:", mouse_x, mouse_y)

                # Switch after 5 clicks
                if len(player1_clicks) >= 5:
                    print("Switching to Player 2...")
                    reveal1 = False

            # PLAYER 2 TURN
            else:
                player2_clicks.append((mouse_x, mouse_y))
                print("P2 click:", mouse_x, mouse_y)

                # stop after 5 clicks
                if len(player2_clicks) >= 5:
                    print("Player 2 finished placing ships.")

    return True

  
  
# Game loop
running = True
while running:
    # Fill the background
    screen.fill((0,0,0))
    
    reveal_player_ships(reveal1)
        
    pygame.draw.rect(screen, BLUE, (rect_x1, rect_y1, rect_width, rect_height), line_thickness)
    pygame.draw.rect(screen, BLUE, (rect_x2, rect_y1, rect_width, rect_height), line_thickness)
    
    
    running = event_handler()

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()