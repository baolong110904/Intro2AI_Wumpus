import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 850, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")

# Colors
MINT_GREEN = (204, 255, 229)
BUTTON_COLOR = (230, 230, 255)
TEXT_COLOR = (70, 70, 70)

# Load background image
background_image = pygame.image.load("./Assets/game_menu.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create font
font = pygame.font.Font(None, 36)
titlefont = pygame.font.Font(None, 100)

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
buttons = [
    Button(WIDTH//2 - 110, 200, 200, 50, "START"),
    Button(WIDTH//2 - 110, 275, 200, 50, "MAP"),
    Button(WIDTH//2 - 110, 350, 200, 50, "TUTORIAL"),
    Button(WIDTH//2 - 110, 425, 200, 50, "EXIT")
]

# Main game loop
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "EXIT":
                            pygame.quit()
                            sys.exit()
                        elif button.text == "START":
                            return "start_game"
                        elif button.text == "MAP":
                            return "choose_map"
                        elif button.text == "TUTORIAL":
                            return "tutorial"

        # Draw background
        screen.blit(background_image, (0, 0))


        # Draw buttons
        for button in buttons:
            button.draw()

        pygame.display.flip()
def tutorial_screen():
    # Load images (replace with actual file paths)
    agent_img = pygame.image.load("./Assets/agent.png")
    wumpus_img = pygame.image.load("./Assets/wumpus.png")
    gold_img = pygame.image.load("./Assets/gold.png")
    pit_img = pygame.image.load("./Assets/pit.png")
    gas_img = pygame.image.load("./Assets/poison.png")
    potion_img = pygame.image.load("./Assets/potion.png")
    breeze_img = pygame.image.load("./Assets/breeze.png")
    stench_img = pygame.image.load("./Assets/stench.png")
    whiff_img = pygame.image.load("./Assets/whiff.png")
    glow_img = pygame.image.load("./Assets/glow.png")

    # Scale images to a smaller size
    icon_size = (50, 50)
    agent_img = pygame.transform.scale(agent_img, icon_size)
    wumpus_img = pygame.transform.scale(wumpus_img, icon_size)
    gold_img = pygame.transform.scale(gold_img, icon_size)
    pit_img = pygame.transform.scale(pit_img, icon_size)
    gas_img = pygame.transform.scale(gas_img, icon_size)
    potion_img = pygame.transform.scale(potion_img, icon_size)
    breeze_img = pygame.transform.scale(breeze_img, icon_size)
    stench_img = pygame.transform.scale(stench_img, icon_size)
    whiff_img = pygame.transform.scale(whiff_img, icon_size)
    glow_img = pygame.transform.scale(glow_img, icon_size)

    font_small = pygame.font.Font(None, 24)  # Smaller font for descriptions

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return

        # Draw background
        screen.fill(MINT_GREEN)

        # Draw title
        title_surf = titlefont.render("Tutorial", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 30))
        screen.blit(title_surf, title_rect)

        # Display elements with brief descriptions and points
        element_positions = [
            (50, 100, agent_img, "Agent: Moves around the grid."),
            (50, 160, wumpus_img, "Wumpus: Kills the agent. Points: -10,000"),
            (50, 220, gold_img, "Gold: The agent’s goal. Points: +5,000"),
            (50, 280, pit_img, "Pit: Agent falls and dies. Points: -10,000"),
            (50, 340, gas_img, "Gas: Reduces health by 25%. No points deducted."),
            (50, 400, potion_img, "Potion: Restores health by 25%. No points added.")
        ]
        for x, y, img, desc in element_positions:
            screen.blit(img, (x, y))
            desc_surf = font_small.render(desc, True, TEXT_COLOR)
            screen.blit(desc_surf, (x + 60, y + 10))

        # Display percepts with brief descriptions
        percept_positions = [
            (450, 100, breeze_img, "Breeze: Near a pit."),
            (450, 160, stench_img, "Stench: Near a Wumpus."),
            (450, 220, whiff_img, "Whiff: Near poisonous gas."),
            (450, 280, glow_img, "Glow: Near a healing potion.")
        ]
        for x, y, img, desc in percept_positions:
            screen.blit(img, (x, y))
            desc_surf = font_small.render(desc, True, TEXT_COLOR)
            screen.blit(desc_surf, (x + 60, y + 10))

        # Display agent's actions in text form at the bottom
        actions = [
            "Actions:",
            "1. Move Forward: Moves in the current direction. Point: -10",
            "2. Turn Left/Right: Changes the agent's direction. Point: -10",
            "3. Grab: Picks up gold or healing potions.",
            "4. Shoot: Fires an arrow to kill the Wumpus. Point: -100",
            "5. Climb: Exits the cave. Point: +10",
            "6. Heal: Uses a healing potion to restore health."
        ]
        for i, action in enumerate(actions):
            action_surf = font_small.render(action, True, TEXT_COLOR)
            screen.blit(action_surf, (170, 460 + i * 20))

        # Draw back button
        back_button.draw()

        pygame.display.flip()



# Create the back button
back_button = Button(WIDTH - 150, HEIGHT - 70, 120, 50, "BACK")

if __name__ == "__main__":
    action = main_menu()
    if action == "tutorial":
        tutorial_screen()