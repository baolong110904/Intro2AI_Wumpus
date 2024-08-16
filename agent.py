# Define agent directions
FACING_TO_UP = 0
FACING_TO_RIGHT = 1
FACING_TO_DOWN = 2
FACING_TO_LEFT = 3

GRID_SIZE = 80  # Size of each cell in the grid

class Agent:
    def __init__(self):
        self.position = [GRID_SIZE, GRID_SIZE]  # Start at (1,1)
        self.direction = 'UP'  # Start facing up
        self.health = 100
        self.score = 0
        self.arrows = 10
        self.healing_potions = 0

    def move(self, direction, map_size):
        if direction == 'UP' and self.position[1] > 0:
            self.position[1] -= GRID_SIZE
        elif direction == 'DOWN' and self.position[1] + GRID_SIZE < map_size * GRID_SIZE:
            self.position[1] += GRID_SIZE
        elif direction == 'LEFT' and self.position[0] > 0:
            self.position[0] -= GRID_SIZE
        elif direction == 'RIGHT' and self.position[0] + GRID_SIZE < map_size * GRID_SIZE:
            self.position[0] += GRID_SIZE
        else:
            return  # Invalid move

        self.score -= 10  # Moving costs 10 points

    def grab_item(self, cell):
        if 'G' in cell and 'G_L' not in cell:
            self.score += 5000
            return 'G'
        elif 'H_P' in cell:
            self.healing_potions += 1
            return 'H_P'
        return None

    def shoot_arrow(self, map, agent_pos, agent_dir):
        if self.arrows > 0:
            self.arrows -= 1
            self.score -= 100
            # Implement arrow shooting logic
            pass

    def use_potion(self):
        if self.healing_potions > 0:
            self.health = min(100, self.health + 25)
            self.healing_potions -= 1
