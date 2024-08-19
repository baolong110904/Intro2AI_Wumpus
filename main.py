import pygame
from program import Program
from agent import Agent
from ui import GameUI
from menu import main_menu, tutorial_screen  # Make sure these functions are correctly defined in menu.py
import sys

def run_game(map_file):
    program = Program(map_file)
    agent = Agent()
    map_size = program.map_size

    # Initialize the UI
    ui = GameUI(map_size)
    clock = pygame.time.Clock()

    while True:
        ui.handle_events()

        info = program.report_cell(agent.pos)
        action = agent.act(info, map_size)

        if action:
            print(action)
            response_info = program.verify_action(action)

            if response_info:
                print(response_info)

            if response_info == 'AGENT_CLIMBED' or response_info == 'AGENT_DIED':
                ui.show_game_over(program.point)
                break

            agent.react(response_info, map_size)
            ui.update_explored_cells(agent.pos)

        # Update the UI
        ui.draw(program, agent)
        clock.tick(5)  # Limit to 5 FPS for better visualization

    print(f'POINT {program.point}')

def map_selection_screen():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Select Map")

    # Colors and fonts
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.Font(None, 36)

    # Load map images
    map_images = [pygame.image.load(f"./Assets/map{i}.png").convert() for i in range(1, 6)]
    map_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in map_images]

    current_map_index = 0
    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(map_images[current_map_index], (0, 0))
        prev_button = font.render("Previous", True, BLACK)
        next_button = font.render("Next", True, BLACK)
        start_button = font.render("Return", True, BLACK)

        screen.blit(prev_button, (50, HEIGHT - 50))
        screen.blit(next_button, (WIDTH - 150, HEIGHT - 50))
        screen.blit(start_button, (WIDTH // 2 - 100, HEIGHT - 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 < x < 150 and HEIGHT - 50 < y < HEIGHT - 10:
                    current_map_index = (current_map_index - 1) % 5
                elif WIDTH - 150 < x < WIDTH - 50 and HEIGHT - 50 < y < HEIGHT - 10:
                    current_map_index = (current_map_index + 1) % 5
                elif WIDTH // 2 - 100 < x < WIDTH // 2 + 100 and HEIGHT - 50 < y < HEIGHT - 10:
                    return current_map_index  # Return the selected map index


def main():
    pygame.init()
    selected_map_index = None  # Store the selected map index

    while True:
        action = main_menu()
        if action == "start_game":
            if selected_map_index is None:
                # Prompt user to select a map if not selected yet
                selected_map_index = map_selection_screen()  # Get the map index
            map_file = f"map{selected_map_index + 1}.txt"  # Map file based on index
            run_game(map_file)
        elif action == "choose_map":
            selected_map_index = map_selection_screen()  # Get the map index
        elif action == "tutorial":
            tutorial_screen()
        elif action == "quit":
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
