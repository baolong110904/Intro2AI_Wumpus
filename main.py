# main.py
from program import Program
from agent import Agent
from ui import GameUI
from menu import *
import pygame

def count_remaining_gold(program):
    return sum('G' in cell for row in program.map for cell in row)

def run_game():
    program = Program('map4.txt')
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

if __name__ == '__main__':
    pygame.init()
    while True:
        action = main_menu()
        if action == "start_game":
            run_game()
        elif action == "choose_map":
            # Add logic to choose a map
            pass
        elif action == "tutorial":
            # Add logic to show the tutorial
            pass