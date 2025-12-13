
##NEW CODE
import pygame
import os

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

# --- INITIALIZATION ---
pygame.init()
pygame.font.init()

# Fonts
font = pygame.font.SysFont('Arial', 24)
instr_font = pygame.font.SysFont('Arial', 20)
winner_font = pygame.font.SysFont('Arial', 40, bold=True)

# Screen dimensions
screen_width = 1000
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battleship Dashboard")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_BLUE = (0, 100, 255)

# Board Properties
rect_x1 = 50
rect_y1 = 50
rect_width = 400
rect_height = 400
line_thickness = 5 
rect_x2 = rect_x1 + rect_width + 20
CELL_SIZE = 20

# UI Buttons
button_instr_rect = pygame.Rect(50, 500, 200, 50)
button_quit_rect = pygame.Rect(270, 500, 200, 50)
button_restart_rect = pygame.Rect(490, 500, 200, 50)

# Game State
reveal1 = True
in_battle = False
game_over = False
current_player = 1 
current_orientation = 'horizontal' # 'horizontal' or 'vertical'

# End/Reveal Phase State
reveal_phase = False          # True when showing final ship locations
reveal_start_time = 0         # time reveal started (ms)
REVEAL_DURATION = 8000      # 8 seconds in milliseconds
WIN_SCORE = 1700              # game ends if someone reaches this

# Temporary per-player reveal (after 5th ship placement)
reveal_temp = False
reveal_temp_target = None  # 'player1' or 'player2'
reveal_temp_end_time = 0
REVEAL_MS = 3000  # ms to show player's final placement


# Instruction Scroll State
show_instructions = False
scroll_y = 0

# Data Structures
# Grids: (x,y): True/False/Hit/Miss
player1_grid = {(x, y): False for x in range(20) for y in range(20)}
player2_grid = {(x, y): False for x in range(20) for y in range(20)}

player1_battle_grid = {(x, y): None for x in range(20) for y in range(20)}
player2_battle_grid = {(x, y): None for x in range(20) for y in range(20)}

# Store ships as: (x, y, orientation, size)
player1_ships_data = [] 
player2_ships_data = []

ship_sizes = [5, 4, 3, 3, 2] 

# --- FILE I/O ---
def get_instructions():
    """Reads lines from instructions.txt safely."""
    try:
        if os.path.exists("instructions.txt"):
            with open("instructions.txt", "r") as f:
                content = f.readlines()
            return [line.strip() for line in content]
        else:
            return ["Error: instructions.txt not found.", "Please create the file."]
    except Exception as e:
        return [f"Error reading file: {e}"]

instruction_lines = get_instructions()

# --- SCORING ---
def calculate_score(player_num):
    """
    Placeholder score function.
    Logic: Counts total 'hits' on the enemy board.
    """
    score = 0
    # Determine which grid tracks this player's attacks
    if player_num == 1:
        target_grid = player1_battle_grid
    else:
        target_grid = player2_battle_grid

    for x in range(20):
        for y in range(20):
            if target_grid.get((x,y)) == "hit":
                score += 100
    return score

# --- LOGIC FUNCTIONS ---

def save_ship_placement(gx, gy, player_num):
    """Validates and saves a ship placement with rotation."""
    global current_orientation
    
    # Point to correct player data
    if player_num == 1:
        existing_ships = player1_ships_data
        grid = player1_grid
    else:
        existing_ships = player2_ships_data
        grid = player2_grid
        
    idx = len(existing_ships)
    if idx >= len(ship_sizes): return False 
    
    size = ship_sizes[idx]
    
    # 1. Check Bounds & Overlap
    if current_orientation == 'horizontal':
        if gx + size > 20: 
            print("Out of bounds (Horizontal)")
            return False
        for i in range(size):
            if grid.get((gx + i, gy)) is True or grid.get((gx + i, gy)) == "Y":
                return False
    else: # vertical
        if gy + size > 20: 
            print("Out of bounds (Vertical)")
            return False
        for i in range(size):
            if grid.get((gx, gy + i)) is True or grid.get((gx, gy + i)) == "Y":
                return False

    # 2. Save Data
    existing_ships.append((gx, gy, current_orientation, size))
    
    # 3. Update Grid (Visuals)
    grid[(gx, gy)] = "Y" # Head
    if current_orientation == 'horizontal':
        for i in range(size):
            if gx+i < 20: grid[(gx+i, gy)] = True
    else:
        for i in range(size):
            if gy+i < 20: grid[(gx, gy+i)] = True
            
    return True

def handle_battle_click(mx, my):
    """Handles shooting logic."""
    global current_player
    
    # Set targets
    if current_player == 1:
        target_x, target_y = rect_x2, rect_y1
        my_battle_grid = player1_battle_grid
        enemy_grid = player2_grid
    else:
        target_x, target_y = rect_x1, rect_y1
        my_battle_grid = player2_battle_grid
        enemy_grid = player1_grid
        
    # Check bounds
    if mx < target_x or mx > target_x + rect_width or my < target_y or my > target_y + rect_height:
        return False
        
    gx = (mx - target_x) // CELL_SIZE
    gy = (my - target_y) // CELL_SIZE
    
    # Check if already clicked
    if my_battle_grid.get((gx, gy)) is not None:
        print("Already attacked here!")
        return False
        
    # Check Hit or Miss
    if enemy_grid.get((gx, gy)) is True or enemy_grid.get((gx, gy)) == "Y":
        my_battle_grid[(gx, gy)] = "hit"
        print("HIT!")
    else:
        my_battle_grid[(gx, gy)] = "miss"
        print("MISS!")
        
    # Switch turns
    current_player = 2 if current_player == 1 else 1

    # --- WIN CHECK ---
    p1_score = calculate_score(1)
    p2_score = calculate_score(2)
    if p1_score >= WIN_SCORE or p2_score >= WIN_SCORE:
        start_reveal_phase()

    return True

def quit_game_early():
    """Ends game, calculates winner, displays result."""
    global game_over, in_battle
    
    game_over = True
    in_battle = False
    
    p1_score = calculate_score(1)
    p2_score = calculate_score(2)
    
    return p1_score, p2_score
    
def start_reveal_phase():
    """Starts 33-second reveal of both boards before final score screen."""
    global reveal_phase, reveal_start_time, in_battle
    reveal_phase = True
    reveal_start_time = pygame.time.get_ticks()
    in_battle = False  # freeze battle while revealing

    
##RESET GAME DEFINOTION

def reset_game():
    """Resets all game state to start a fresh match."""
    global reveal1, in_battle, game_over, current_player, current_orientation
    global reveal_phase, reveal_start_time
    global show_instructions, scroll_y
    global player1_grid, player2_grid, player1_battle_grid, player2_battle_grid
    global player1_ships_data, player2_ships_data
    global p1_final_score, p2_final_score

    # Game State
    reveal1 = True
    in_battle = False
    game_over = False
    current_player = 1
    current_orientation = 'horizontal'
    reveal_phase = False
    reveal_start_time = 0

    # Instructions overlay state
    show_instructions = False
    scroll_y = 0

    # Fresh empty grids
    player1_grid = {(x, y): False for x in range(20) for y in range(20)}
    player2_grid = {(x, y): False for x in range(20) for y in range(20)}

    player1_battle_grid = {(x, y): None for x in range(20) for y in range(20)}
    player2_battle_grid = {(x, y): None for x in range(20) for y in range(20)}

    # Clear ships
    player1_ships_data = []
    player2_ships_data = []

    # Reset final scores shown on game over screen
    p1_final_score = 0
    p2_final_score = 0





# --- DRAWING FUNCTIONS ---

def draw_instructions_overlay():
    """Draws instructions with a scrolling window."""
    # Semi-transparent bg
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    
    # Box parameters
    box_x, box_y = 100, 50
    box_w, box_h = 800, 500
    padding = 20
    
    # Draw container
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_w, box_h))
    pygame.draw.rect(screen, BLUE, (box_x, box_y, box_w, box_h), 5)
    
    title = font.render("INSTRUCTIONS (Scroll to read)", True, BLUE)
    screen.blit(title, (box_x + padding, box_y + padding))
    
    # --- SCROLLING LOGIC ---
    # Define the viewing area (clip)
    view_rect = pygame.Rect(box_x + padding, box_y + 60, box_w - 2*padding, box_h - 80)
    screen.set_clip(view_rect) # Only draw pixels inside this box
    
    start_y = box_y + 60 + scroll_y # Apply scroll offset
    line_height = 30
    
    for line in instruction_lines:
        text_surf = instr_font.render(line, True, BLACK)
        screen.blit(text_surf, (box_x + padding, start_y))
        start_y += line_height
        
    screen.set_clip(None) # Reset clip so we can draw other things normally
    # -----------------------
    
    close_text = font.render("Press 'I' to Close", True, RED)
    screen.blit(close_text, (box_x + padding, box_y + box_h + 10))

def draw_grid(surface, x0, y0, reveal=False, player_name='', battle=False, final_reveal=False):
    """Draws the grid, ships, and battle marks."""
    
    # 1. Base Grid
    for x in range(20):
        for y in range(20):
            rect = pygame.Rect(x0 + x*CELL_SIZE, y0 + y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(surface, WHITE, rect)
            
      # --- FINAL REVEAL MODE ---
    if final_reveal:
        # pick correct ship grid + enemy battle grid
        if player_name == "player1":
            ship_grid = player1_grid
            enemy_battle = player2_battle_grid  # p2 hit p1 ships
        else:
            ship_grid = player2_grid
            enemy_battle = player1_battle_grid  # p1 hit p2 ships

        for x in range(20):
            for y in range(20):
                val = ship_grid.get((x, y))
                if val is True or val == "Y":  # ship exists here
                    rect = pygame.Rect(x0 + x*CELL_SIZE, y0 + y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                    if enemy_battle.get((x, y)) == "hit":
                        pygame.draw.rect(surface, BLACK, rect)   # hit ships = black
                    else:
                        pygame.draw.rect(surface, GREEN, rect)   # unhit ships = green
        return  # stop here so normal drawing doesn't override
          

    # 2. Battle Marks (Hits/Misses)
    if battle:
        grid_to_show = player1_battle_grid if player_name == "player2" else player2_battle_grid
        for x in range(20):
            for y in range(20):
                state = grid_to_show.get((x, y))
                rect = pygame.Rect(x0 + x*CELL_SIZE, y0 + y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                if state == "hit":
                    pygame.draw.rect(surface, BLACK, rect)
                elif state == "miss":
                    pygame.draw.rect(surface, DARK_BLUE, rect)

    # 3. Ships (Placement Phase)
    elif reveal and not battle:
        # Pick correct grid
        target_grid = player1_grid if player_name == "player1" else player2_grid
        
        for x in range(20):
            for y in range(20):
                val = target_grid.get((x, y))
                rect = pygame.Rect(x0 + x*CELL_SIZE, y0 + y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                if val == "Y":
                    pygame.draw.rect(surface, YELLOW, rect)
                elif val is True:
                    pygame.draw.rect(surface, RED, rect)

    # 4. Hide Enemy Ships
    elif not reveal and not battle:
        rect = pygame.Rect(x0, y0, CELL_SIZE*20, CELL_SIZE*20)
        pygame.draw.rect(surface, BLACK, rect)
        msg = font.render("Opponent View", True, WHITE)
        screen.blit(msg, (x0+120, y0+180))

# --- MAIN LOOP ---

def main():
    global reveal1, in_battle, game_over, current_player, current_orientation
    global show_instructions, scroll_y, reveal_phase, reveal_start_time
    global p1_final_score, p2_final_score, reveal_temp, reveal_temp_target, reveal_temp_end_time

    running = True
    p1_final_score = 0
    p2_final_score = 0

    while running:
        screen.fill((30, 30, 30))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL and show_instructions:
                scroll_y += event.y * 20
                if scroll_y > 0: scroll_y = 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    show_instructions = not show_instructions
                elif event.key == pygame.K_r and not in_battle:
                    current_orientation = 'vertical' if current_orientation == 'horizontal' else 'horizontal'
                elif event.key == pygame.K_UP and show_instructions:
                    scroll_y += 20
                elif event.key == pygame.K_DOWN and show_instructions:
                    scroll_y -= 20

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Button Checks
                if button_instr_rect.collidepoint(mx, my):
                    show_instructions = not show_instructions

                elif button_quit_rect.collidepoint(mx, my) and not game_over:
                    p1_final_score, p2_final_score = quit_game_early()

                elif button_restart_rect.collidepoint(mx, my):
                    reset_game()

                elif show_instructions or reveal_phase or game_over or reveal_temp:
                    pass  # ignore grid clicks (also ignore during temporary reveal)

                # Game Logic
                elif in_battle:
                    handle_battle_click(mx, my)

                else:
                    # Placement Logic
                    if reveal1 and rect_x1 <= mx <= rect_x1+rect_width and rect_y1 <= my <= rect_y1+rect_height:
                        gx = (mx - rect_x1) // CELL_SIZE
                        gy = (my - rect_y1) // CELL_SIZE
                        if save_ship_placement(gx, gy, 1):
                            if len(player1_ships_data) == 5:
                                # Show Player 1's final placement briefly before switching to Player 2
                                reveal_temp = True
                                reveal_temp_target = 'player1'
                                reveal_temp_end_time = pygame.time.get_ticks() + REVEAL_MS
                                current_orientation = 'horizontal'

                    elif (not reveal1) and rect_x2 <= mx <= rect_x2+rect_width and rect_y1 <= my <= rect_y1+rect_height:
                        gx = (mx - rect_x2) // CELL_SIZE
                        gy = (my - rect_y1) // CELL_SIZE
                        if save_ship_placement(gx, gy, 2):
                            if len(player2_ships_data) == 5:
                                # Show Player 2's final placement briefly before entering battle
                                reveal_temp = True
                                reveal_temp_target = 'player2'
                                reveal_temp_end_time = pygame.time.get_ticks() + REVEAL_MS

        # --- REVEAL TIMER CHECK (MUST BE HERE) ---
        if reveal_phase:
            if pygame.time.get_ticks() - reveal_start_time >= REVEAL_DURATION:
                reveal_phase = False
                game_over = True
                p1_final_score = calculate_score(1)
                p2_final_score = calculate_score(2)

        # Temporary per-player reveal expiration
        if reveal_temp:
            if pygame.time.get_ticks() >= reveal_temp_end_time:
                # If Player 1 was being shown, toggle to Player 2 placement
                if reveal_temp_target == 'player1':
                    reveal_temp = False
                    reveal_temp_target = None
                    reveal1 = False
                # If Player 2 was being shown, start battle
                elif reveal_temp_target == 'player2':
                    reveal_temp = False
                    reveal_temp_target = None
                    in_battle = True

        # --- DRAWING ---
        
        if game_over:
            # Game Over Screen
            screen.fill(BLACK)
            txt = winner_font.render("GAME OVER", True, WHITE)
            screen.blit(txt, (screen_width//2 - 100, 150))
            
            score_txt = font.render(f"P1 Score: {p1_final_score}   vs   P2 Score: {p2_final_score}", True, BLUE)
            screen.blit(score_txt, (screen_width//2 - 150, 250))
            
            if p1_final_score > p2_final_score:
                res = "Player 1 Wins!"
                col = RED
            elif p2_final_score > p1_final_score:
                res = "Player 2 Wins!"
                col = GREEN
            else:
                res = "It's a Tie!"
                col = WHITE
                
            res_txt = winner_font.render(res, True, col)
            screen.blit(res_txt, (screen_width//2 - 120, 350))
            # Restart button on Game Over screen
            pygame.draw.rect(screen, GREEN, button_restart_rect)
            screen.blit(font.render("Restart", True, BLACK), (button_restart_rect.x + 60, button_restart_rect.y + 10))
            
        else:
            # Standard Game Drawing
            if reveal_phase:
                draw_grid(screen, rect_x1, rect_y1, player_name="player1", final_reveal=True)
                draw_grid(screen, rect_x2, rect_y1, player_name="player2", final_reveal=True)

            elif reveal_temp:
                # Show only the target player's final placement during temporary reveal
                if reveal_temp_target == 'player1':
                    draw_grid(screen, rect_x1, rect_y1, player_name="player1", final_reveal=True)
                    draw_grid(screen, rect_x2, rect_y1, player_name="player2", reveal=False)
                else:
                    draw_grid(screen, rect_x1, rect_y1, player_name="player1", reveal=False)
                    draw_grid(screen, rect_x2, rect_y1, player_name="player2", final_reveal=True)

            else:
                draw_grid(screen, rect_x1, rect_y1, reveal1, "player1", in_battle)
                draw_grid(screen, rect_x2, rect_y1, not reveal1, "player2", in_battle)
            
            # Borders
            pygame.draw.rect(screen, BLUE, (rect_x1, rect_y1, rect_width, rect_height), line_thickness)
            pygame.draw.rect(screen, BLUE, (rect_x2, rect_y1, rect_width, rect_height), line_thickness)
            
            # Buttons
            pygame.draw.rect(screen, GRAY, button_instr_rect)
            pygame.draw.rect(screen, RED, button_quit_rect)
            pygame.draw.rect(screen, GREEN, button_restart_rect)

            screen.blit(font.render("Instructions (I)", True, BLACK), (button_instr_rect.x + 20, button_instr_rect.y + 10))
            screen.blit(font.render("Quit Early", True, WHITE), (button_quit_rect.x + 45, button_quit_rect.y + 10))
            screen.blit(font.render("Restart", True, BLACK), (button_restart_rect.x + 60, button_restart_rect.y + 10))

            
            # Info Text
            if in_battle:
                info = f"Player {current_player}'s Turn to Attack!"
                col = GREEN
            else:
                p_turn = "Player 1" if reveal1 else "Player 2"
                info = f"{p_turn} Placing Ships. Orientation: {current_orientation.upper()} (Press R)"
                col = YELLOW
            
            screen.blit(font.render(info, True, col), (300, 20))
            
            if show_instructions:
                draw_instructions_overlay()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

