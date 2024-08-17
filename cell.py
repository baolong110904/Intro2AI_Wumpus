from enum import Enum

class Element(Enum):
    GOLD = 'G'
    PIT = 'P'
    WUMPUS = 'W'
    BREEZE = 'B'
    STENCH = 'S'
    AGENT = 'A'
    HEALING_POTION = 'H_P'
    POISONOUS_GAS = 'P_G'
    WHIFF = 'W_H'        # Percept indicating nearby poisonous gas
    GLOW = 'G_L'        # Percept indicating nearby healing potion
    EMPTY = '-'

class Tile:
    def __init__(self, grid_position, grid_size, content_str):
        # Initializing the grid position and related attributes
        self.grid_position = grid_position  # (row, col)
        self.grid_size = grid_size
        self.tile_position = self.compute_tile_position(grid_position)
        self.index = self.compute_index(self.tile_position)

        # Exploration status and percepts
        self.visited = False
        self.percepts = {
            'gold': False,
            'pit': False,
            'wumpus': False,
            'breeze': False,
            'stench': False,
            'healing_potion': False,
            'poisonous_gas': False,
            'whiff': False,
            'glow': False
        }

        # Initialize the tile's contents
        self.parse_contents(content_str)
        self.previous_tile = None
        self.next_tiles = []

    def compute_tile_position(self, grid_position):
        # Convert matrix coordinates to more human-readable coordinates
        return (grid_position[1] + 1, self.grid_size - grid_position[0])

    def compute_index(self, tile_position):
        # Calculate the unique index based on the tile position
        return self.grid_size * (tile_position[1] - 1) + tile_position[0]

    def parse_contents(self, content_str):
        # Parse the contents of the tile and set the corresponding percepts
        for char in content_str:
            if char == Element.GOLD.value:
                self.percepts['gold'] = True
            elif char == Element.PIT.value:
                self.percepts['pit'] = True
            elif char == Element.WUMPUS.value:
                self.percepts['wumpus'] = True
            elif char == Element.BREEZE.value:
                self.percepts['breeze'] = True
            elif char == Element.STENCH.value:
                self.percepts['stench'] = True
            elif char == Element.HEALING_POTION.value:
                self.percepts['healing_potion'] = True
            elif char == Element.POISONOUS_GAS.value:
                self.percepts['poisonous_gas'] = True
            elif char == Element.WHIFF.value:
                self.percepts['whiff'] = True
            elif char == Element.GLOW.value:
                self.percepts['glow'] = True

    # Define the checks for each percept
    def has_gold(self):
        return self.percepts['gold']

    def has_pit(self):
        return self.percepts['pit']

    def has_wumpus(self):
        return self.percepts['wumpus']

    def has_breeze(self):
        return self.percepts['breeze']

    def has_stench(self):
        return self.percepts['stench']

    def has_healing_potion(self):
        return self.percepts['healing_potion']

    def has_poisonous_gas(self):
        return self.percepts['poisonous_gas']

    def has_whiff(self):
        return self.percepts['whiff']

    def has_glow(self):
        return self.percepts['glow']

    def is_safe(self):
        # Determines whether the tile is safe to move into (no pits, wumpus, or gas)
        return not self.has_pit() and not self.has_wumpus() and not self.has_poisonous_gas()

    def set_previous_tile(self, tile):
        # Sets the previous tile (for pathfinding or exploration tracking)
        self.previous_tile = tile

    def clear_gold(self):
        # Removes gold from the tile
        self.percepts['gold'] = False

    def defeat_wumpus(self, tile_matrix, kb):
        # Removes the Wumpus from the tile and updates adjacent tiles' stench
        self.percepts['wumpus'] = False
        self.update_adjacent_tiles(tile_matrix, kb, 'stench')

    def update_adjacent_tiles(self, tile_matrix, kb, percept_type):
        # Updates the percepts in adjacent tiles (e.g., removing stench after Wumpus is defeated)
        adjacent_tiles = self.get_adjacent_tiles(tile_matrix)
        for adjacent_tile in adjacent_tiles:
            if percept_type == 'stench':
                adjacent_tile.percepts['stench'] = False
            elif percept_type == 'breeze':
                adjacent_tile.percepts['breeze'] = False
            elif percept_type == 'whiff':
                adjacent_tile.percepts['whiff'] = False
            elif percept_type == 'glow':
                adjacent_tile.percepts['glow'] = False
            # Example: Update knowledge base after percept change
            kb.update_knowledge(adjacent_tile)

    def get_adjacent_tiles(self, tile_matrix):
        # Determine adjacent tiles based on the current position
        adjacent_tiles = []
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for direction in directions:
            adj_position = (self.grid_position[0] + direction[0], self.grid_position[1] + direction[1])
            if 0 <= adj_position[0] < self.grid_size and 0 <= adj_position[1] < self.grid_size:
                adjacent_tiles.append(tile_matrix[adj_position[0]][adj_position[1]])
        return adjacent_tiles

    def mark_visited(self):
        # Marks the tile as visited
        self.visited = True

    def update_next_tiles(self, valid_adjacent_tiles):
        # Updates the list of possible next tiles for the agent to explore
        for tile in valid_adjacent_tiles:
            if tile.previous_tile is None:
                self.next_tiles.append(tile)
                tile.set_previous_tile(self)

    def to_literal(self, element: Element, positive=True):
        # Convert the tile's element state to a literal for logical inference
        factor = 10 ** len(str(self.grid_size * self.grid_size))
        index_value = self.index
        literal_value = element.value * factor + index_value
        if not positive:
            literal_value *= -1
        return literal_value
