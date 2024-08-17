import pygame
from ui import *
from program import *
from agent import Agent

def run_game():
    pygame.init()

    program = Program('map1.txt')
    map_size, map = program.get_map()
    grid_size = GRID_SIZE

    WIDTH = map_size * grid_size + 250
    HEIGHT = max(map_size * grid_size, 400)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wumpus World")

    images = load_images(grid_size, ASSETS_PATH)

    agent = Agent()
    remaining_golds = count_golds(map)

    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    handle_keydown(event, agent, map, map_size, remaining_golds, screen)

        if not game_over:
            check_game_status(agent, map, remaining_golds, screen)

            # Fill screen with background color
            screen.fill((255, 255, 255))

            # Display the map
            display_map(screen, map, images, grid_size, agent.position, agent.direction)

            # Display HUD
            display_hud(screen, agent.score, remaining_golds, agent.health, agent.healing_potions)

            pygame.display.flip()

    pygame.quit()

def handle_keydown(event, agent, map, map_size, remaining_golds, screen):
    if event.key == pygame.K_UP:
        agent.move('UP', map_size)
    elif event.key == pygame.K_DOWN:
        agent.move('DOWN', map_size)
    elif event.key == pygame.K_LEFT:
        agent.move('LEFT', map_size)
    elif event.key == pygame.K_RIGHT:
        agent.move('RIGHT', map_size)
    elif event.key == pygame.K_SPACE:  # Grab
        row = agent.position[1] // GRID_SIZE
        col = agent.position[0] // GRID_SIZE
        cell = map[row][col]
        grabbed_item = agent.grab_item(cell)
        if grabbed_item == 'G':
            remaining_golds -= 1
            map[row][col] = cell.replace('G', '', 1)
        elif grabbed_item == 'H_P':
            map[row][col] = cell.replace('H_P', '', 1)
    elif event.key == pygame.K_s:  # Shoot
        agent.shoot_arrow(map, agent.position, agent.direction)
    elif event.key == pygame.K_c:  # Climb
        if agent.position == [GRID_SIZE, GRID_SIZE] and remaining_golds == 0:
            agent.score += 10
            display_win_screen(screen)
            return False
    elif event.key == pygame.K_p:  # Use healing potion
        agent.use_potion()

    return True

def check_game_status(agent, map, remaining_golds, screen):
    current_cell = get_cell_content(map, agent.position)

    if 'P' in current_cell and 'P_G' not in current_cell:
        agent.score -= 10000
        display_lose_screen(screen, "You fell into a pit!")
        return False
    elif 'W' in current_cell and 'W_H' not in current_cell:
        agent.score -= 10000
        display_lose_screen(screen, "You were killed by the Wumpus!")
        return False
    elif 'P_G' in current_cell:
        agent.health -= 25
        if agent.health <= 0:
            display_lose_screen(screen, "You died from poisonous gas!")
            return False

    return True

def get_cell_content(map, agent_pos):
    row = agent_pos[1] // GRID_SIZE
    col = agent_pos[0] // GRID_SIZE

    if 0 <= row < len(map) and 0 <= col < len(map[0]):
        return map[row][col]
    else:
        return ''  # Return an empty string if the agent is out of bounds
