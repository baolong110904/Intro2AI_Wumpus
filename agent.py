GRID_SIZE = 80  # Size of each cell in the grid

from program import *
from cell import *
from PropositionalLogic import *

class AgentAction:
    # Movement Directions
    FACING_TO_UP = 0
    FACING_TO_RIGHT = 1
    FACING_TO_DOWN = 2
    FACING_TO_LEFT = 3
    MOVE_FORWARD = 4

    # Interactions
    GRAB_GOLD = 5
    GRAB_HEALING_POTION = 6
    FIRE_ARROW = 7
    
    # Percepts
    SENSE_BREEZE = 8
    SENSE_STENCH = 9
    SENSE_SCREAM = 10
    SENSE_WHIFF = 11
    SENSE_GLOW = 12
    
    # Inferences
    INFER_SAFE = 13
    INFER_PIT = 14
    INFER_WUMPUS = 15
    INFER_POISONOUS_GAS = 16
    INFER_HEALING_POTION = 17

    # Additional Actions
    BE_EATEN_BY_WUMPUS = 18
    FALL_INTO_PIT = 19
    BREATHING_POISONOUS_GAS = 20
    USING_HEALING_POTION = 21
    CLIMB_OUT_OF_THE_CAVE = 22
    KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD = 23

    # Detection
    DETECT_PIT = 24
    DETECT_NO_PIT = 25
    
    DETECT_WUMPUS = 26
    DETECT_NO_WUMPUS = 27
    
    DETECT_POISONOUS_GAS = 28
    DETECT_NO_POISONOUS_GAS = 29
    
    DETECT_HEALING_POTION = 30
    DETECT_NO_HEALING_POTION = 31
    
class Agent:
    def __init__(self, input_file, output_file):
        # Agent specifications:
        self.position = [GRID_SIZE, GRID_SIZE]  # Start at (1,1)
        self.direction = AgentAction.FACING_TO_UP  # Start facing up
        
        self.health = 100
        self.score = 0
        self.alive = True
        
        # Agent learning
        self.map = Program
        self.knowledge_base = PropositionalLogic
        
        self.path = []
        self.actions_list = []
        self.score = 0
        
        # Writing agent action to output file
        self.input_file = input_file
        self.output_file = output_file
        
    def move(self, direction, ):
        if direction == AgentAction.FACING_TO_UP and self.position[1] > 0:
            self.position[1] -= GRID_SIZE
        elif direction == AgentAction.FACING_TO_DOWN and self.position[1] + GRID_SIZE < self.map.get_map_size() * GRID_SIZE:
            self.position[1] += GRID_SIZE
        elif direction == AgentAction.FACING_TO_LEFT and self.position[0] > 0:
            self.position[0] -= GRID_SIZE
        elif direction == AgentAction.FACING_TO_RIGHT and self.position[0] + GRID_SIZE < self.map.get_map_size() * GRID_SIZE:
            self.position[0] += GRID_SIZE
        else:
            return None # Invalid move
        self.score -= 10  # Moving costs 10 points

    def add_event(self, event: str):
        write_file = open(self.output_file, 'a')
        write_file.write(event + '\n')
        write_file.close()
    
    def output_event(self, action):
        self.actions_list.append(action)
        print(action)
        
        if action == AgentAction.FACING_TO_UP: # 0
            self.add_event(str(AgentAction.FACING_TO_UP))
            
        elif action == AgentAction.FACING_TO_DOWN: # 2
            self.add_event(str(AgentAction.FACING_TO_DOWN))
            
        elif action == AgentAction.FACING_TO_LEFT: # 3
            self.add_event(str(AgentAction.FACING_TO_LEFT))
            
        elif action == AgentAction.FACING_TO_RIGHT: # 1
            self.add_event(str(AgentAction.FACING_TO_RIGHT))
            
        elif action == AgentAction.MOVE_FORWARD: # 4
            self.score -= 10
            print("Score: ", str(self.score))
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.MOVE_FORWARD))
            
        elif action == AgentAction.GRAB_GOLD: # 5
            self.score += 5000
            print("Score: ", str(self.score))
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.GRAB_GOLD))
            
        elif action == AgentAction.GRAB_HEALING_POTION: # 6
            self.health += 25
            self.add_event("Health: " + str(self.health) + " " + str(AgentAction.GRAB_HEALING_POTION))
            
        elif action == AgentAction.FIRE_ARROW: # 7
            self.score -= 10
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.FIRE_ARROW))
            
        elif action == AgentAction.SENSE_BREEZE: # 8
            self.add_event(str(AgentAction.SENSE_BREEZE))
            
        elif action == AgentAction.SENSE_STENCH: # 9
            self.add_event(str(AgentAction.SENSE_STENCH))
            
        elif action == AgentAction.SENSE_WHIFF: # 10
            self.add_event(str(AgentAction.SENSE_WHIFF))
            
        elif action == AgentAction.SENSE_SCREAM: # 12
            self.add_event(str(AgentAction.SENSE_SCREAM))

        elif action == AgentAction.SENSE_GLOW: # 11
            self.add_event(str(AgentAction.SENSE_GLOW))
            
        elif action == AgentAction.INFER_SAFE: # 13
            self.add_event(str(AgentAction.INFER_SAFE))
            
        elif action == AgentAction.INFER_PIT: # 14
            self.add_event(str(AgentAction.INFER_PIT))
            
        elif action == AgentAction.INFER_POISONOUS_GAS: # 16
            self.add_event(str(AgentAction.INFER_POISONOUS_GAS))
            
        elif action == AgentAction.INFER_WUMPUS: # 15
            self.add_event(str(AgentAction.INFER_WUMPUS))
            
        elif action == AgentAction.INFER_HEALING_POTION: # 17
            self.add_event(str(AgentAction.INFER_HEALING_POTION))

        elif action == AgentAction.BE_EATEN_BY_WUMPUS: # 18
            self.score -= 10000
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.BE_EATEN_BY_WUMPUS))

        elif action == AgentAction.FALL_INTO_PIT: # 19
            self.score -= 10000
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.FALL_INTO_PIT))

        elif action == AgentAction.BREATHING_POISONOUS_GAS: # 20
            self.health -= 25
            self.add_event("Health: " + str(self.health) + " " + str(AgentAction.BREATHING_POISONOUS_GAS))

        elif action == AgentAction.USING_HEALING_POTION: # 21
            self.health += 25
            self.add_event("Health: " + str(self.health) + " " + str(AgentAction.USING_HEALING_POTION))

        elif action == AgentAction.CLIMB_OUT_OF_THE_CAVE: # 22
            self.score += 10
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.CLIMB_OUT_OF_THE_CAVE))

        elif action == AgentAction.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD: # 23
            self.score += 5000
            self.add_event('Score: ' + str(self.score) + " " + str(AgentAction.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD))

        elif action == AgentAction.DETECT_PIT: # 24
            self.add_event(str(AgentAction.DETECT_PIT))

        elif action == AgentAction.DETECT_NO_PIT: # 25
            self.add_event(str(AgentAction.DETECT_NO_PIT))

        elif action == AgentAction.DETECT_WUMPUS: # 26
            self.add_event(str(AgentAction.DETECT_WUMPUS))

        elif action == AgentAction.DETECT_NO_WUMPUS: # 27
            self.add_event(str(AgentAction.DETECT_NO_WUMPUS))

        elif action == AgentAction.DETECT_POISONOUS_GAS: # 28
            self.add_event(str(AgentAction.DETECT_POISONOUS_GAS))

        elif action == AgentAction.DETECT_NO_POISONOUS_GAS: # 29
            self.add_event(str(AgentAction.DETECT_NO_POISONOUS_GAS))

        elif action == AgentAction.DETECT_HEALING_POTION: # 30
            self.add_event(str(AgentAction.DETECT_HEALING_POTION))

        elif action == AgentAction.DETECT_NO_HEALING_POTION: # 31
            self.add_event(str(AgentAction.DETECT_NO_HEALING_POTION))

            
    def execute_action(self, action):
        self.log_action(action)
        if action == AgentAction.MOVE_FORWARD:
            self.score -= 10
        elif action == AgentAction.GRAB_GOLD:
            self.score += 5000
        elif action == AgentAction.FIRE_ARROW:
            self.score -= 100
            
    def update_knowledge(self, tile):
        adjacent_tiles = tile.get_adjacent_tiles(self.tiles)
        
        if tile.has_pit():
            self.knowledge_base.adding_clause([tile.to_literal(Element.WUMPUS, False)])  # Wumpus can't be in a pit

        if tile.has_wumpus():
            self.knowledge_base.adding_clause([tile.to_literal(Element.PIT, False)])  # Pit can't be with Wumpus

        if tile.has_breeze():
            self.knowledge_base.adding_clause([tile.to_literal(Element.BREEZE, True)])  # Breeze implies adjacent pit

        if tile.has_stench():
            self.knowledge_base.adding_clause([tile.to_literal(Element.STENCH, True)])  # Stench implies adjacent Wumpus

        # Update knowledge base logic based on perceptions, similar to the original approach

    def decide_next_move(self):
        # Decision-making based on current knowledge and percepts
        if self.current_tile.has_pit():
            self.execute_action(AgentAction.FALL_INTO_PIT)
            return False

        if self.current_tile.has_wumpus():
            self.execute_action(AgentAction.BE_EATEN_BY_WUMPUS)
            return False

        if self.current_tile.has_gold():
            self.execute_action(AgentAction.GRAB_GOLD)
            self.current_tile.clear_gold()

        if self.current_tile.has_breeze():
            self.execute_action(AgentAction.SENSE_BREEZE)

        if self.current_tile.has_stench():
            self.execute_action(AgentAction.SENSE_STENCH)

        if not self.current_tile.visited:
            self.current_tile.mark_visited()
            self.update_knowledge(self.current_tile)

        valid_moves = self.current_tile.get_adjacent_tiles(self.tiles)

        for next_tile in valid_moves:
            if next_tile.is_safe():
                self.move_to(next_tile)
                if not self.decide_next_move():
                    return False
                self.move_to(self.current_tile)

        return True

    def move_to(self, next_tile):
        self.turn_towards(next_tile)
        self.execute_action(AgentAction.MOVE_FORWARD)
        self.current_tile = next_tile

    def turn_towards(self, next_tile):
        # Determine direction and execute turning action based on the position of the next tile
        if next_tile.grid_position[0] == self.current_tile.grid_position[0]:
            if next_tile.grid_position[1] > self.current_tile.grid_position[1]:
                self.execute_action(AgentAction.FACING_TO_RIGHT)
            else:
                self.execute_action(AgentAction.FACING_TO_LEFT)
        elif next_tile.grid_position[1] == self.current_tile.grid_position[1]:
            if next_tile.grid_position[0] > self.current_tile.grid_position[0]:
                self.execute_action(AgentAction.FACING_TO_DOWN)
            else:
                self.execute_action(AgentAction.FACING_TO_UP)

    def backtrack(self):
        if not self.decide_next_move():
            return False
        return True

    def solve_wumpus_world(self):
        with open(self.output_file, 'w') as file:
            pass  # Clear the output file

        self.backtrack()

        victory_flag = True
        for row in self.tiles:
            for tile in row:
                if tile.has_gold() or tile.has_wumpus():
                    victory_flag = False
                    break
        if victory_flag:
            self.execute_action(AgentAction.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)

        if self.current_tile.grid_position == [0, 0]:  # Assuming this is the start position
            self.execute_action(AgentAction.CLIMB_OUT_OF_THE_CAVE)

        return self.actions_list
        # Handle other actions similarly
    # def grab_item(self, cell):
    #     if 'G' in cell:  # Gold
    #         self.score += 5000
    #         return 'G'
    #     elif 'H_P' in cell:  # Healing Potion
    #         return 'H_P'
    #     return None
    
    # def shoot_arrow(self):
    #     self.score -= 100

    # def hitting_wumpus_or_pit(self):
    #     self.score -= 10000

    # def use_potion(self):
    #     self.health += 25

    # def get_position(self):
    #     return self.position

    # def get_direction(self):
    #     return self.direction

    # def turn_left(self):
    #     self.direction = (self.direction - 1) % 4

    # def turn_right(self):
    #     self.direction = (self.direction + 1) % 4

    # def get_score(self):
    #     return self.score

    # def get_health(self):
    #     return self.health
    


####### TESTING #######
def run_simulation(map_filename, output_filename):
    # Initialize the world using the Program class
    world = Program(map_filename)
    
    # Get the map and its size from the world
    map_size, game_map = world.get_map()
    
    # Initialize the agent with the input map and output filename
    agent = Agent(map_filename, output_filename)
    
    # Assuming agent starts at (1,1) or similar, depending on your grid setup
    agent.position = [GRID_SIZE, GRID_SIZE]  # Top-left corner of the map
    agent.direction = AgentAction.FACING_TO_UP
    
    # Main simulation loop
    while agent.alive:
        # Get the agent's current tile
        i, j = (agent.position[1] // GRID_SIZE) - 1, (agent.position[0] // GRID_SIZE) - 1
        current_tile = game_map[i][j]
        
        # Perceive the environment and update the agent's knowledge base
        if 'B' in current_tile:
            agent.output_event(AgentAction.SENSE_BREEZE)
        if 'S' in current_tile:
            agent.output_event(AgentAction.SENSE_STENCH)
        if 'W_H' in current_tile:
            agent.output_event(AgentAction.SENSE_WHIFF)
        if 'G_L' in current_tile:
            agent.output_event(AgentAction.SENSE_GLOW)
        
        # Infer safe moves based on the agent's knowledge base
        if current_tile == '-' or current_tile == 'B' or current_tile == 'S' or current_tile == 'W_H' or current_tile == 'G_L':
            agent.output_event(AgentAction.INFER_SAFE)
        
        # Handle possible actions based on inferences
        if 'G' in current_tile:
            agent.output_event(AgentAction.GRAB_GOLD)
            game_map[i][j] = game_map[i][j].replace('G', '')
        
        if 'W' in current_tile:
            agent.output_event(AgentAction.BE_EATEN_BY_WUMPUS)
            agent.alive = False
            break
        
        if 'P' in current_tile:
            agent.output_event(AgentAction.FALL_INTO_PIT)
            agent.alive = False
            break
        
        if 'P_G' in current_tile:
            agent.output_event(AgentAction.BREATHING_POISONOUS_GAS)
            agent.health -= 25
            if agent.health <= 0:
                agent.alive = False
                break
        
        if 'H_P' in current_tile:
            agent.output_event(AgentAction.USING_HEALING_POTION)
            game_map[i][j] = game_map[i][j].replace('H_P', '')
            agent.health += 25
        
        # Move the agent to the next tile (simplified logic, should be based on actual pathfinding or decision-making)
        next_position = None
        if agent.direction == AgentAction.FACING_TO_UP:
            next_position = [agent.position[0], agent.position[1] - GRID_SIZE]
        elif agent.direction == AgentAction.FACING_TO_DOWN:
            next_position = [agent.position[0], agent.position[1] + GRID_SIZE]
        elif agent.direction == AgentAction.FACING_TO_LEFT:
            next_position = [agent.position[0] - GRID_SIZE, agent.position[1]]
        elif agent.direction == AgentAction.FACING_TO_RIGHT:
            next_position = [agent.position[0] + GRID_SIZE, agent.position[1]]
        
        # Ensure the move is within bounds
        if 0 <= next_position[0] < map_size * GRID_SIZE and 0 <= next_position[1] < map_size * GRID_SIZE:
            agent.move(agent.direction)
        else:
            agent.alive = False  # No valid moves, simulation ends
        
    # If the agent is still alive, let it exit the cave
    if agent.alive:
        agent.output_event(AgentAction.CLIMB_OUT_OF_THE_CAVE)

    # Final output
    print(f"Final Score: {agent.score}")
    print(f"Final Health: {agent.health}")
    return agent.score, agent.health

# Example usage
if __name__ == "__main__":
    run_simulation('map1.txt', 'output_testing.txt')