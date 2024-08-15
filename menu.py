import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")

# Colors
MINT_GREEN = (204, 255, 229)
BUTTON_COLOR = (230, 230, 255)
TEXT_COLOR = (70, 70, 70)

# Load images
robot_image = pygame.image.load("./Assets/wumpus_menu.gif")
robot_image2 = pygame.image.load("./Assets/wumpus_menu2.gif")   

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
    red_shift = 0
    green_shift = 85
    blue_shift = 170
    direction = 1
    
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
        screen.fill(MINT_GREEN)
        # screen.blit(background, (0, 0))

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
        for button in buttons:
            button.draw()

        # Draw robot characters
        screen.blit(robot_image, (20, HEIGHT - robot_image.get_height() - 80))  # Left image
        screen.blit(robot_image2, (WIDTH - robot_image2.get_width(), HEIGHT - robot_image2.get_height() - 70))  # Right image

        pygame.display.flip()