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

PLAYER 1: RED SHIPS
PLAYER 2: GREEN SHIPS
WATER - BLUE
HIT - BLACK

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
GREEN = (0,255,0)

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
in_battle = False
current_player = 1  # Track whose turn it is (1 or 2)

#Initialize plater grids: (x,y):False (no ship) or True (ship)
player1_grid = {(x, y): False for x in range(20) for y in range(20)}
player2_grid = {(x, y): False for x in range(20) for y in range(20)}

# Track battle state: {(x, y): "hit" or "miss"}
player1_battle_grid = {(x, y): None for x in range(20) for y in range(20)}
player2_battle_grid = {(x, y): None for x in range(20) for y in range(20)}

player1_clicks = []
player2_clicks = []

#battleship sizes
ship_sizes = [5, 4, 3, 3, 2] 

#draw the grid for battleships

ship_blocks = []

def battle_players(surface, x0, y0, reveal=False, player_name=''):
    if player_name == "player1":
        opponent_grid = player2_grid
        battle_grid = player1_battle_grid  # tracks what player1 has discovered
    else:
        opponent_grid = player1_grid
        battle_grid = player2_battle_grid  # tracks what player2 has discovered

    for x in range(20):
        for y in range(20):
            cell_state = battle_grid.get((x, y))
            if cell_state is not None:  # Only draw if this cell has been clicked
                leftwall = x0 + x * CELL_SIZE
                topwall = y0 + y * CELL_SIZE
                rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                
                if cell_state == "hit":
                    pygame.draw.rect(surface, BLACK, rect)
                elif cell_state == "miss":
                    pygame.draw.rect(surface, (0, 100, 255), rect)  # dark blue for miss

def draw_grid(surface, x0, y0, ship_size=0, reveal=False, player_name='', battle=False):
    if battle:
        # During battle, show white grid + battle results (hits/misses)
        for x in range(20):
            for y in range(20):
                leftwall = x0 + x * CELL_SIZE
                topwall = y0 + y * CELL_SIZE
                rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                pygame.draw.rect(surface, WHITE, rect)
        
        # Draw hits/misses based on which player's grid this is
        if player_name == "player2":
            # This is player 2's grid—show player 1's attacks
            for x in range(20):
                for y in range(20):
                    state = player1_battle_grid.get((x, y))
                    if state is not None:
                        leftwall = x0 + x * CELL_SIZE
                        topwall = y0 + y * CELL_SIZE
                        rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                        if state == "hit":
                            pygame.draw.rect(surface, BLACK, rect)
                        elif state == "miss":
                            pygame.draw.rect(surface, (0, 100, 255), rect)
        else:
            # This is player 1's grid—show player 2's attacks
            for x in range(20):
                for y in range(20):
                    state = player2_battle_grid.get((x, y))
                    if state is not None:
                        leftwall = x0 + x * CELL_SIZE
                        topwall = y0 + y * CELL_SIZE
                        rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                        if state == "hit":
                            pygame.draw.rect(surface, BLACK, rect)
                        elif state == "miss":
                            pygame.draw.rect(surface, (0, 100, 255), rect)
    elif reveal:
        # Choose which grid to read from
        if player_name == "player1":
            grid = player1_grid
            clicks = player1_clicks
        else:
            grid = player2_grid
            clicks = player2_clicks

        if battle:
            # During battle, only show white grid (opponent's ships hidden, grid data preserved)
            for x in range(20):
                for y in range(20):
                    leftwall = x0 + x * CELL_SIZE
                    topwall = y0 + y * CELL_SIZE
                    rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)
                    pygame.draw.rect(surface, WHITE, rect)
                    
                    
        else:
            # During placement, show ship previews
            #Update grid dictionary based on clicks - only process the last click for preview
            if clicks:
                click_x, click_y = clicks[-1]  # Get only the most recent click
                gx = (click_x - x0) // CELL_SIZE
                gy = (click_y - y0) // CELL_SIZE

                if gx >= 0 and gx < 20 and gy >= 0 and gy < 20:
                    # Decide ship direction based on position
                    if gx < 20 - ship_size + 1:  
                        # Normal left to right
                        for i in range(ship_size):
                            sx = gx + i
                            if sx < 20:
                                grid[(sx, gy)] = True
                    else:
                        # Backwards right to left
                        for i in range(ship_size):
                            sx = gx - i
                            if sx >= 0:
                                grid[(sx, gy)] = True
                    
                    # Store the starting click with yellow
                    grid[(gx, gy)] = "Y"

            for x in range(20):
                for y in range(20):
                    leftwall = x0 + x * CELL_SIZE
                    topwall = y0 + y * CELL_SIZE
                    rect = pygame.Rect(leftwall, topwall, CELL_SIZE - 1, CELL_SIZE - 1)

                    # Default white cell
                    pygame.draw.rect(surface, WHITE, rect)

                    # Draw yellow for starting clicks first
                    if grid[(x, y)] == "Y" and not battle:
                        pygame.draw.rect(surface, YELLOW, rect)
                        # print("YELLOW CALLED")
                    # Draw red for ship blocks (but not if it's yellow)
                    elif grid[(x, y)] is True and not battle:
                        pygame.draw.rect(surface, RED, rect)

    else:
        rect = pygame.Rect(x0, y0, CELL_SIZE*20-1, CELL_SIZE*20-1)
        pygame.draw.rect(surface, BLACK, rect)
        text_surface = font.render('It is not your turn yet!', True, WHITE)
        screen.blit(text_surface, (x0+100, y0+190))

#TODO
# def rotateblocks():

#hit = black
#miss = blue - dark blue - ocean
# def battle_logic(player,)
    
def reveal_player_ships(reveal1,in_battle=False):
    if(reveal1):
        # Player 1's turn
        text_surface = font.render('Player 1, place your ships!', True, (255, 255, 255))
        screen.blit(text_surface, (rect_x1, rect_y1-40))  
        
        #after rect_y1 - > 5 - ship size to be replaced.
        # choose the current ship size based on how many ships already placed
        idx = len(player1_clicks)
        if idx < len(ship_sizes):
            current_size = ship_sizes[idx-1]
        else:
            current_size = ship_sizes[-1]   
        draw_grid(screen, rect_x1, rect_y1, current_size, reveal1, "player1", in_battle)
        draw_grid(screen, rect_x2, rect_y1, 0, False, "player2", in_battle)
    else:
        # Player 2's turn
        text_surface = font.render('Player 2, place your ships!', True, (255, 255, 255))
        screen.blit(text_surface, (rect_x2, rect_y1-40))  
        # choose the current ship size for player2
        idx2 = len(player2_clicks)
        if idx2 < len(ship_sizes):
            current_size2 = ship_sizes[idx2-1]
        else:
            current_size2 = ship_sizes[-1]
        draw_grid(screen, rect_x1, rect_y1, 0, False, "player1", in_battle)
        draw_grid(screen, rect_x2, rect_y1, current_size2, True, "player2",in_battle) 
   
def has_beenclicked(mx, my, clicks,player_name):
    # Check if click is within grid boundaries
    if(player_name == "player1"):
        if mx < rect_x1 or mx > rect_x1 + rect_width or my < rect_y1 or my > rect_y1 + rect_height:
            return True
        # Get grid cell coordinates
        gx = (mx - rect_x1) // CELL_SIZE
        gy = (my - rect_y1) // CELL_SIZE
        # Check if cell is blue or yellow (already has ship)
        if player1_grid[(gx, gy)] is True or player1_grid[(gx, gy)] == "Y":
            return True
        
    elif(player_name == "player2"):
        if mx < rect_x2 or mx > rect_x2 + rect_width or my < rect_y1 or my > rect_y1 + rect_height:
            return True
        # Get grid cell coordinates
        gx = (mx - rect_x2) // CELL_SIZE
        gy = (my - rect_y1) // CELL_SIZE
        # Check if cell is blue or yellow (already has ship)
        if player2_grid[(gx, gy)] is True or player2_grid[(gx, gy)] == "Y":
            return True
    
    return False

def handle_battle_click(mx, my):
    """Process a click during battle mode. Returns True if click was valid."""
    global current_player
    
    if current_player == 1:
        # Player 1 attacks player 2's grid (on the right)
        if mx < rect_x2 or mx > rect_x2 + rect_width or my < rect_y1 or my > rect_y1 + rect_height:
            return False
        
        gx = (mx - rect_x2) // CELL_SIZE
        gy = (my - rect_y1) // CELL_SIZE
        
        if gx < 0 or gx >= 20 or gy < 0 or gy >= 20:
            return False
        
        # Check if already attacked this cell
        if player1_battle_grid[(gx, gy)] is not None:
            print("Player 1: Already attacked this cell!")
            return False
        
        # Check if opponent has a ship there
        if player2_grid[(gx, gy)] is True or player2_grid[(gx, gy)] == "Y":
            player1_battle_grid[(gx, gy)] = "hit"
            print(f"Player 1: HIT at ({gx}, {gy})!")
        else:
            player1_battle_grid[(gx, gy)] = "miss"
            print(f"Player 1: MISS at ({gx}, {gy})!")
        
        current_player = 2
        return True
    
    else:
        # Player 2 attacks player 1's grid (on the left)
        if mx < rect_x1 or mx > rect_x1 + rect_width or my < rect_y1 or my > rect_y1 + rect_height:
            return False
        
        gx = (mx - rect_x1) // CELL_SIZE
        gy = (my - rect_y1) // CELL_SIZE
        
        if gx < 0 or gx >= 20 or gy < 0 or gy >= 20:
            return False
        
        # Check if already attacked this cell
        if player2_battle_grid[(gx, gy)] is not None:
            print("Player 2: Already attacked this cell!")
            return False
        
        # Check if opponent has a ship there
        if player1_grid[(gx, gy)] is True or player1_grid[(gx, gy)] == "Y":
            player2_battle_grid[(gx, gy)] = "hit"
            print(f"Player 2: HIT at ({gx}, {gy})!")
        else:
            player2_battle_grid[(gx, gy)] = "miss"
            print(f"Player 2: MISS at ({gx}, {gy})!")
        
        current_player = 1
        return True

def event_handler():
    global mouse_x, mouse_y, reveal1, in_battle

    #Display mouse coordinates    
    x_coord, y_coord = pygame.mouse.get_pos()
    mouse_text = font.render(f' X,Y:({x_coord}, {y_coord})', True, WHITE)
    screen.blit(mouse_text, (800,500))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
         
            if in_battle:
                # During battle, process attacks
                handle_battle_click(mouse_x, mouse_y)
            
            elif len(player2_clicks) > 5:
                in_battle = True
                print("Both players have finished placing ships.")
                print("COORDINATE",mouse_x,mouse_y)
                
                
            # PLAYER 1 TURN
            elif reveal1:
                
                if has_beenclicked(mouse_x, mouse_y, player1_clicks,"player1"):
                    print("Player 1 already clicked this cell. Choose another.")
                    continue
                player1_clicks.append((mouse_x, mouse_y))
                print("P1 click:", mouse_x, mouse_y)
                
                # Shows the 5th click BEFORE switching
                if len(player1_clicks) == 5:
                    # Immediately redraw the screen so the new click is visible
                    screen.fill((0,0,0))
                    
                    reveal_player_ships(reveal1)  # draw current (player1) grid with the new click
                    pygame.draw.rect(screen, BLUE, (rect_x1, rect_y1, rect_width, rect_height), line_thickness)
                    pygame.draw.rect(screen, BLUE, (rect_x2, rect_y1, rect_width, rect_height), line_thickness)
                    # Also update mouse coordinates display (optional, keeps UI consistent)
                    x_coord2, y_coord2 = pygame.mouse.get_pos()
                    mouse_text2 = font.render(f' X,Y:({x_coord2}, {y_coord2})', True, WHITE)
                    screen.blit(mouse_text2, (800,500))
                    pygame.display.flip()
                    pygame.time.delay(500)
                    reveal1 = False

            # PLAYER 2 TURN
            else:
                if has_beenclicked(mouse_x, mouse_y, player2_clicks,"player2"):
                    print("Player 2 already clicked this cell. Choose another.")
                    continue
                player2_clicks.append((mouse_x, mouse_y))
                print("P2 click:", mouse_x, mouse_y)

                # stop after 5 clicks
                if len(player2_clicks) == 6:
                    in_battle = True
                    print("Both players have finished placing ships.")
                    print("Player 2 finished placing ships.")
                    ship_count = sum(1 for v in player2_grid.values() if v is True)
                    print(ship_count)
                    
                    

    return True

def show_instructions():
    instructions = open("instructions.txt", "r").read()
    print(instructions)
# Game loop
running = True
while running:
    
    # Fill the background
    screen.fill((0,0,0))
    
    reveal_player_ships(reveal1, in_battle)
    
    # Show battle status
    if in_battle:
        status_text = font.render(f'Player {current_player}\'s Turn - Click opponent grid to attack!', True, (255, 200, 100))
        screen.blit(status_text, (150, 480))
        
    pygame.draw.rect(screen, BLUE, (rect_x1, rect_y1, rect_width, rect_height), line_thickness)
    pygame.draw.rect(screen, BLUE, (rect_x2, rect_y1, rect_width, rect_height), line_thickness)
    
    
    running = event_handler()

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
