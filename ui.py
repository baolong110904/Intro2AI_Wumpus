# ui.py
import pygame
import sys
from enum import Enum
from agent import *
from program import *

class CARD(Enum):
    BREEZE = 0
    BUSH = 1
    EMPTY = 2
    GOLD = 3
    PIT = 4
    HEALING_POTION = 5
    GLOW = 6
    POISONOUS_GAS = 7
    WHIFF = 8
    STENCH = 9
    WUMPUS = 10
    START = 11
    AGENT = 12

pygame.init()

WIDTH, HEIGHT = 1400, 600
GRID_SIZE = 600
SIDEBAR_WIDTH = WIDTH - GRID_SIZE
CELL_SIZE = GRID_SIZE // 10  # Assuming a 10x10 grid

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Load images
card_images = [pygame.image.load(f"./Assets/{img}").convert_alpha() for img in [
    "breeze.png", "bush.png", "empty.png", "gold.png", "pit.png",
    "potion.png", "glow.png", "poison.png", "whiff.png", "stench.png",
    "wumpus.png", "exit.png", "agent.png"
]]
card_images = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in card_images]

# Load and rotate agent images
agent_images = [pygame.transform.rotate(card_images[CARD.AGENT.value], angle) for angle in [270, 180, 90, 0]]

# Load and scale the background image
bg_image = pygame.image.load("./Assets/bg.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)

class GameUI:
    def __init__(self, map_size):
        self.map_size = map_size
        self.cell_size = GRID_SIZE // map_size
        self.explored_cells = set()
        self.removed_items = set()

    def draw(self, program, agent):
        screen.blit(bg_image, (0, 0))
        
        # Draw grid
        for row in range(self.map_size):
            for col in range(self.map_size):
                cell_info = program.map[row][col]
                x, y = col * self.cell_size, row * self.cell_size
                
                if (row, col) not in self.explored_cells:
                    screen.blit(card_images[CARD.BUSH.value], (x, y))
                else:
                    # Draw empty cell as base
                    screen.blit(card_images[CARD.EMPTY.value], (x, y))
                    
                    if (row, col) == agent.pos:
                        screen.blit(agent_images[agent.dir], (x, y))
                    elif 'W' in cell_info:
                        screen.blit(card_images[CARD.WUMPUS.value], (x, y))
                    elif 'P' in cell_info:
                        screen.blit(card_images[CARD.PIT.value], (x, y))
                    elif 'G' in cell_info and f'G{row}{col}' not in self.removed_items:
                        screen.blit(card_images[CARD.GOLD.value], (x, y))
                    elif 'H_P' in cell_info and f'H_P{row}{col}' not in self.removed_items:
                        screen.blit(card_images[CARD.HEALING_POTION.value], (x, y))
                    elif 'P_G' in cell_info:
                        screen.blit(card_images[CARD.POISONOUS_GAS.value], (x, y))
                    elif 'W_H' in cell_info:
                        screen.blit(card_images[CARD.WHIFF.value], (x, y))
                    elif 'G_L' in cell_info:
                        screen.blit(card_images[CARD.GLOW.value], (x, y))
                    elif 'S' in cell_info and f'S{row}{col}' not in self.removed_items:
                        screen.blit(card_images[CARD.STENCH.value], (x, y))
                    elif 'B' in cell_info:
                        screen.blit(card_images[CARD.BREEZE.value], (x, y))

        
        # Draw board
        pygame.draw.rect(screen, LIGHT_BLUE, (GRID_SIZE, 0, SIDEBAR_WIDTH, HEIGHT))
        
        # Display points
        point_text = font.render(f"Points: {program.point}", True, BLACK)
        screen.blit(point_text, (GRID_SIZE + 20, 20))

        # # Display remaining gold
        # gold_text = font.render(f"Remaining Gold: {remaining_gold}", True, BLACK)
        # screen.blit(gold_text, (GRID_SIZE, 60))

        # Display health
        health_percentage = (agent.hp / 100) * 100  # Assuming max HP is 100
        health_text = font.render(f"Health: {health_percentage:.0f}%", True, BLACK)
        screen.blit(health_text, (GRID_SIZE + 20, 100))

        pygame.display.flip()

    def update_explored_cells(self, pos):
        self.explored_cells.add(pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def show_game_over(self, point):
        # Initialize the display
        screen = pygame.display.get_surface()  # Use the existing screen surface
        WIDTH, HEIGHT = screen.get_size()  # Get the screen dimensions
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        LIGHT_GREY = (211, 211, 211)

        # Load and scale background image
        background = pygame.image.load("./Assets/bg_1.png").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Define fonts
        title_font = pygame.font.Font(None, 72)
        score_font = pygame.font.Font(None, 60)

        # Render text with shadow for better visibility
        game_over_text = title_font.render("Agent has climbed out!", True, RED)
        game_over_shadow = title_font.render("Agent has climbed out!", True, BLACK)
        score_text = score_font.render(f"Final Score: {point}", True, WHITE)
        score_shadow = score_font.render(f"Final Score: {point}", True, BLACK)

        # Get text positions
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        game_over_shadow_rect = game_over_shadow.get_rect(center=(WIDTH//2 + 3, HEIGHT//2 - 47))
        score_text_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        score_shadow_rect = score_shadow.get_rect(center=(WIDTH//2 + 3, HEIGHT//2 + 53))

        # Draw shadow and then text to create a 3D effect
        screen.blit(game_over_shadow, game_over_shadow_rect)
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(score_shadow, score_shadow_rect)
        screen.blit(score_text, score_text_rect)

        # Display everything
        pygame.display.flip()

        pygame.time.wait(3000)  # Wait for 3 seconds

        # Return to main menu or restart game
        self.return_to_main_menu()  # Assuming you have this method implemented

    def return_to_main_menu(self):
        # Logic to return to the main menu
        pass
    def update_explored_cells(self, pos):
        self.explored_cells.add(pos)

    def remove_item(self, item, pos):
        self.removed_items.add(f"{item}{pos[0]}{pos[1]}")


# if __name__ == '__main__':
#     program = Program('map4.txt')
#     agent = Agent()
#     draw(program, agent)