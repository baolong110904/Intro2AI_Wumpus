import pygame
from agent import *

# Define constants
MAP_FILE_PATH = 'map1.txt'
ASSETS_PATH = './Assets/'

def load_images(grid_size, assets_path):
    images = {
        'A': pygame.image.load(assets_path + "agent.png"),
        'G': pygame.image.load(assets_path + "gold.png"),
        'B': pygame.image.load(assets_path + "breeze.png"),
        'P': pygame.image.load(assets_path + "pit.png"),
        'S': pygame.image.load(assets_path + "stench.png"),
        'W': pygame.image.load(assets_path + "wumpus.png"),
        'P_G': pygame.image.load(assets_path + "poison.png"),
        'H_P': pygame.image.load(assets_path + "potion.png"),
        'W_H': pygame.image.load(assets_path + "whiff.png"),
        'G_L': pygame.image.load(assets_path + "glow.png"),
        'E': pygame.image.load(assets_path + "exit.png"),
        '-': pygame.image.load(assets_path + "empty.png"),
    }

    # Resize images to fit the grid size
    for key in images:
        images[key] = pygame.transform.scale(images[key], (grid_size, grid_size))
    
    return images

# def load_map(file_path):
#     with open(file_path, 'r') as file:
#         n = int(file.readline().strip()) # Read the size
#         map_data = [line.strip().split('.') for line in file]
#     return map_data

def count_golds(map_data):
    gold_count = 0
    for row in map_data:
        for cell in row:
            percepts = cell.split(',')
            if 'G' in percepts and 'P_G' not in percepts and 'G_L' not in percepts:
                gold_count += 1
    return gold_count


def display_map(screen, map_data, images, grid_size, agent_pos, agent_dir):
    num_rows = len(map_data)
    num_cols = len(map_data[0])

    for row_idx, row in enumerate(map_data):
        for col_idx, cell in enumerate(row):
            x = col_idx * grid_size
            y = row_idx * grid_size

            # Split the cell by comma and draw each image
            percepts = cell.split(',')
            for percept in percepts:
                if percept in images:
                    screen.blit(images[percept], (x, y))
    
    # Draw the agent at its current position and direction
    agent_x, agent_y = agent_pos
    agent_image = images['A']

    # Rotate agent image based on direction
    if agent_dir == FACING_TO_UP:
        agent_image = pygame.transform.rotate(agent_image, 0)
    elif agent_dir == FACING_TO_DOWN:
        agent_image = pygame.transform.rotate(agent_image, 180)
    elif agent_dir == FACING_TO_RIGHT:
        agent_image = pygame.transform.rotate(agent_image, 270)
    elif agent_dir == FACING_TO_LEFT:
        agent_image = pygame.transform.rotate(agent_image, 90)

    # Draw the agent image in its new orientation
    screen.blit(agent_image, (agent_x, agent_y))

def display_win_screen(screen):
    # Fill the screen with a background color
    screen.fill((0, 0, 0))  # Black background

    font = pygame.font.Font(None, 74)
    text = font.render('You Win!', True, (0, 255, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)

    # Add instructions to exit
    font_small = pygame.font.Font(None, 36)
    exit_text = font_small.render('Press ESC to exit', True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    screen.blit(exit_text, exit_rect)

    pygame.display.flip()

    # Wait for the user to exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
    return True

def display_lose_screen(screen, message):
    # Fill the screen with a background color
    screen.fill((0, 0, 0))  # Black background

    font = pygame.font.Font(None, 74)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)

    # Add instructions to exit
    font_small = pygame.font.Font(None, 36)
    exit_text = font_small.render('Press ESC to exit', True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
    screen.blit(exit_text, exit_rect)

    pygame.display.flip()

    # Wait for the user to exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
    return True

def display_hud(screen, score, arrows, remaining_golds, health, healing_potions):
    # Set up the font
    font = pygame.font.Font(None, 36)
    
    # Create a surface for the HUD
    hud_width = 250
    hud_height = screen.get_height()
    hud_surface = pygame.Surface((hud_width, hud_height))
    hud_surface.fill((220, 220, 220))  # Light gray background
    
    # Render the text
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    arrow_text = font.render(f"Arrow: {arrows}", True, (0, 0, 0))
    gold_text = font.render(f"Remaining Golds: {remaining_golds}", True, (0, 0, 0))
    health_text = font.render(f"Health: {health}%", True, (0, 0, 0))
    potion_text = font.render(f"Potions: {healing_potions}", True, (0, 0, 0))
    
    # Position the text on the HUD surface
    hud_surface.blit(score_text, (10, 10))
    hud_surface.blit(arrow_text, (10, 50))
    hud_surface.blit(gold_text, (10, 90))
    hud_surface.blit(health_text, (10, 130))
    hud_surface.blit(potion_text, (10, 170))
    
    # Draw the HUD on the right side of the screen
    screen.blit(hud_surface, (screen.get_width() - hud_width, 0))