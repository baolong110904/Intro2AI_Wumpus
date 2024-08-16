from configs import *

class Agent:
    def __init__(self, program):
        self.program = program
        self.health = FULL_HEALTH  # Full health is 100%
        self.gold_collected = 0
        self.position = START_POSITION  # Assuming the agent starts at position (0, 0)
        self.direction = 'N'  # Assuming the agent starts facing North
        self.alive = True
        self.score = 0
        self.knowledge_base = {}  # To store information about the world

    def get_percepts(self):
        percepts = self.program.get_cell_info(self.position)
        return percepts

    def update_knowledge_base(self, percepts):
        self.knowledge_base[self.position] = percepts
        # Logic to update knowledge base based on percepts goes here

    def decide_action(self):
        # Implement logic to decide the next action
        action = 'Move Forward'  # Placeholder action
        return action

    def perform_action(self, action):
        if action == 'Move Forward':
            self.move_forward()
        elif action == 'Turn Left':
            self.turn_left()
        elif action == 'Turn Right':
            self.turn_right()
        elif action == 'Grab':
            self.grab()
        elif action == 'Shoot':
            self.shoot()
        elif action == 'Heal':
            self.heal()
        elif action == 'Climb':
            self.climb()

    def move_forward(self):
        """
        Move the agent forward in the direction it is currently facing.
        """
        # Implement logic to update the position based on the current direction
        if self.direction == 'N':
            self.position = (self.position[0] - 1, self.position[1])
        elif self.direction == 'S':
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == 'E':
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == 'W':
            self.position = (self.position[0], self.position[1] - 1)
        self.score -= 10  # Penalty for moving
        self.check_current_cell()

    def turn_left(self):
        direction_map = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.direction = direction_map[self.direction]
        self.score -= 10  # Penalty for turning

    def turn_right(self):
        direction_map = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.direction = direction_map[self.direction]
        self.score -= 10  # Penalty for turning

    def grab(self):
        cell_info = self.program.get_cell_info(self.position)
        if 'Gold' in cell_info:
            self.gold_collected += 1
            self.score += 5000
            # Remove gold from the cell after grabbing
            self.program.update_cell(self.position, '-')
        if 'Healing Potion' in cell_info:
            self.health = min(100, self.health + 25)
            # Remove healing potion from the cell after grabbing
            self.program.update_cell(self.position, '-')
        self.score -= 10  # Penalty for grabbing

    def shoot(self):
        # Implement logic to shoot an arrow and check if Wumpus is killed
        self.score -= 100  # Penalty for shooting
        wumpus_killed = self.program.shoot_arrow(self.position, self.direction)
        if wumpus_killed:
            self.program.update_map_after_wumpus_death()
            self.program.scream()

    def heal(self):
        self.health = min(100, self.health + 25)
        self.score -= 10  # Penalty for healing

    def climb(self):
        self.score += 10  # Bonus for climbing out
        print("Agent has climbed out of the cave with score:", self.score)
        self.alive = False  # End the game

    def check_current_cell(self):
        cell_info = self.program.get_cell_info(self.position)
        if 'Wumpus' in cell_info:
            self.die("Wumpus")
        elif 'Pit' in cell_info:
            self.die("Pit")
        elif 'Poisonous Gas' in cell_info:
            self.health -= 25
            if self.health <= 0:
                self.die("Poisonous Gas")

    def die(self, cause):
        print(f"Agent died due to {cause}. Final score: {self.score}")
        self.alive = False
        self.score -= 10000  # Penalty for dying

    def explore(self):
        while self.alive:
            percepts = self.get_percepts()
            self.update_knowledge_base(percepts)
            action = self.decide_action()
            self.perform_action(action)
