import pygame
from ui import *

def run_game():
    pygame.init()
    
    # Load map and calculate dimensions
    map_data = load_map(MAP_FILE_PATH)
    num_rows = len(map_data)
    num_cols = len(map_data[0])
    grid_size = GRID_SIZE  # Grid size is the size of each cell

    # Calculate the screen size based on grid size and number of rows/cols
    WIDTH = num_cols * grid_size + 250  # Add 200 for the HUD width
    HEIGHT = max(num_rows * grid_size, 400) 

    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wumpus World")

    # Load and resize images
    images = load_images(grid_size, ASSETS_PATH)

    # Initialize agent's position and direction
    agent_pos = [GRID_SIZE, GRID_SIZE]  # Position at (1,1) in pixel space
    agent_dir = FACING_TO_UP  # Start facing down

    # Add variables to track game state
    game_over = False
    score = 0
    health = 100
    arrows = 10
    healing_potions = 0
    remaining_golds = count_golds(map_data)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        if agent_dir == FACING_TO_UP and agent_pos[1] > 0:
                            agent_pos[1] -= grid_size
                            score -= 10
                        else:
                            agent_dir = FACING_TO_UP
                    elif event.key == pygame.K_DOWN:
                        if agent_dir == FACING_TO_DOWN and agent_pos[1] + grid_size < num_rows * grid_size:
                            agent_pos[1] += grid_size
                            score -= 10
                        else:
                            agent_dir = FACING_TO_DOWN
                    elif event.key == pygame.K_LEFT:
                        if agent_dir == FACING_TO_LEFT and agent_pos[0] > 0:
                            agent_pos[0] -= grid_size
                            score -= 10
                        else:
                            agent_dir = FACING_TO_LEFT
                    elif event.key == pygame.K_RIGHT:
                        if agent_dir == FACING_TO_RIGHT and agent_pos[0] + grid_size < num_cols * grid_size:
                            agent_pos[0] += grid_size
                            score -= 10
                        else:
                            agent_dir = FACING_TO_RIGHT
                    elif event.key == pygame.K_SPACE:  # Grab
                        score, remaining_golds, healing_potions = grab_item(map_data, agent_pos, score, remaining_golds, healing_potions)
                    elif event.key == pygame.K_s:  # Shoot
                        if arrows > 0:
                            shoot_arrow(map_data, agent_pos, agent_dir)
                            arrows -= 1
                            score -= 100
                    elif event.key == pygame.K_c:  # Climb
                        if agent_pos == [GRID_SIZE, GRID_SIZE] and remaining_golds == 0:
                            score += 10
                            game_over = True
                            running = display_win_screen(screen)
                    elif event.key == pygame.K_p:  # Use healing potion
                        if healing_potions > 0:
                            health = min(100, health + 25)
                            healing_potions -= 1

        if not game_over:
            # Check for win condition
            if agent_pos == [GRID_SIZE, GRID_SIZE] and remaining_golds == 0:
                score += 10
                game_over = True
                running = display_win_screen(screen)
            else:
                # Check for game over conditions
                current_cell = get_cell_content(map_data, agent_pos)
                
                if 'p' in current_cell or 'w' in current_cell:
                    score -= 10000
                    game_over = True
                    running = display_lose_screen(screen, "You died!")
                elif 'm' in current_cell:  # Poisonous gas
                    health -= 25
                    if health <= 0:
                        game_over = True
                        running = display_lose_screen(screen, "You died from poisoning!")
                
                if not game_over:
                    # Fill screen with background color
                    screen.fill((255, 255, 255))  # White background

                    # Display the map
                    display_map(screen, map_data, images, grid_size, agent_pos, agent_dir)

                    # Display HUD
                    display_hud(screen, score, arrows, remaining_golds, health, healing_potions)

                    # Update the display
                    pygame.display.flip()
    pygame.quit()
################################# GAME LOGIC #################################
def grab_item(map_data, agent_pos, score, remaining_golds, healing_potions):
    row = agent_pos[1] // GRID_SIZE
    col = agent_pos[0] // GRID_SIZE
    cell = map_data[row][col]
    
    if 'g' in cell:
        score += 5000
        remaining_golds -= 1
        map_data[row][col] = cell.replace('g', '', 1)
    elif 'h' in cell:
        healing_potions += 1
        map_data[row][col] = cell.replace('h', '', 1)
    
    return score, remaining_golds, healing_potions

def shoot_arrow(map_data, agent_pos, agent_dir):
    # Implement arrow shooting logic
    pass

def get_cell_content(map_data, agent_pos):
    row = agent_pos[1] // GRID_SIZE
    col = agent_pos[0] // GRID_SIZE
    
    # Check if row and col are within valid grid bounds
    if 0 <= row < len(map_data) and 0 <= col < len(map_data[0]):
        return map_data[row][col]
    else:
        return ''  # Return an empty string if the agent is out of bounds
