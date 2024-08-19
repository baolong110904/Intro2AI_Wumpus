# main.py
from program import Program
from agent import Agent
from ui import GameUI
from menu import *
import pygame
import sys

def count_remaining_gold(program):
    return sum('G' in cell for row in program.map for cell in row)

def run_game(fileName):
    program = Program(fileName)
    agent = Agent()
    map_size = program.map_size

    # Initialize the UI
    ui = GameUI(map_size)
    clock = pygame.time.Clock()

    remaining_gold = count_remaining_gold(program)

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
            elif response_info == 'G_EXIST':
                remaining_gold -= 1
            
            agent.react(response_info, map_size)
             # Update explored cells after the agent moves
            ui.update_explored_cells(agent.pos)

        # Update the UI
        ui.draw(program, agent, remaining_gold)
        clock.tick(5)  # Limit to 5 FPS for better visualization

    print(f'POINT {program.point}')

# Main game loop
def main_menu():
    red_shift = 0
    green_shift = 85
    blue_shift = 170
    direction = 1
    playing = False
    map_preview = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playing:
                    for button in levels:
                        if button.is_clicked(event.pos):
                            if button.text == "MAP 1":
                                return run_game("map1.txt")
                            elif button.text == "MAP 2":
                                return run_game("map2.txt")
                            elif button.text == "MAP 3":
                                return run_game("map3.txt")
                            elif button.text == "MAP 4":
                                return run_game("map4.txt")
                            elif button.text == "MAP 5":
                                return run_game("map5.txt")
                # elif map_preview:
                #     for button in maps:
                #         if button.is_clicked(event.pos):
                            # if button.text == "MAP 1":
                            #     preview_map("map1.txt")
                            # elif button.text == "MAP 2":
                            #     preview_map("map2.txt")
                            # elif button.text == "MAP 3":
                            #     preview_map("map3.txt")
                            # elif button.text == "MAP 4":
                            #     preview_map("map4.txt")
                            # elif button.text == "MAP 5":
                            #     preview_map("map5.txt")
                else:
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "EXIT":
                                pygame.quit()
                                sys.exit()
                            elif button.text == "START":
                                playing = True  # Switch to level selection mode
                            elif button.text == "MAP":
                                map_preview = True
                            elif button.text == "TUTORIAL":
                                return "tutorial"

        # Draw background
        screen.fill(MINT_GREEN)

        # Draw title
        title_color = (
            abs((red_shift) % 255),
            abs((green_shift) % 255),
            abs((blue_shift) % 255)
        )
        title = titlefont.render("Wumpus World", True, title_color)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Update color shift
        red_shift += 0.5 * direction
        green_shift += 0.5 * direction
        blue_shift += 0.5 * direction

        if red_shift >= 255 or red_shift <= 0:
            direction *= -1

        # Draw buttons
        if playing:
            for button in levels:
                button.draw()
        elif map_preview:
            for button in maps:
                button.draw()
        else:
            for button in buttons:
                button.draw()

        # Draw robot characters
        screen.blit(robot_image, (20, HEIGHT - robot_image.get_height() - 80))  # Left image
        screen.blit(robot_image2, (WIDTH - robot_image2.get_width(), HEIGHT - robot_image2.get_height() - 70))  # Right image

        pygame.display.flip()
        
if __name__ == '__main__':
    pygame.init()
    action = main_menu()
