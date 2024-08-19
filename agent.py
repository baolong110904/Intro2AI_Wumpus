from program import Program
from utils import *

class Agent:
  def __init__(self):
    # Status
    self.pos = (0, 0)
    self.dir = 0
    self.hp = 100
    self.heal = 0
    # Knowledge
    self.kb = set()
    self.explored_cells = {(0, 0)}
    self.safe_cells = {(0, 0)}
    self.poison_cells = set()
    # Action
    self.intention = []

  def act(self, info: list[str], map_size: int):
    if self.intention:
      # If there is pending action, do it
      action = self.intention.pop(0)
      if action == 'MOVE':
        offset = move_map[self.dir]
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        self.explored_cells.add(self.pos)
        return f'MOVE_{self.pos[0]}_{self.pos[1]}_{self.hp}'
      elif action == 'RIGHT':
        self.dir = (self.dir + 1) % 4
        return 'RIGHT'
      elif action == 'LEFT':
        self.dir = (4 + self.dir - 1) % 4
        return 'LEFT'
      elif action == 'GRAB' or action == 'CLIMB':
        return f'{action}_{self.pos[0]}_{self.pos[1]}'
      elif action == 'SHOOT':
        offset = move_map[self.dir]
        shoot_pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        return f'SHOOT_{shoot_pos[0]}_{shoot_pos[1]}'
      elif action == 'HEAL':
        if self.heal > 0:
          self.heal -= 1
          self.hp += 25
        return 'HEAL'
    else:
      # If there is no pending action, create new
      self.percept(info, map_size)
      self.think(map_size)
  
  def react(self, response, map_size: int):
    # React to response info from program
    if response == 'G_EXIST':
      self.kb.difference_update({f'G{self.pos[0]}{self.pos[1]}'})
    elif response == 'HP_EXIST':
      self.heal += 1
    elif response == 'PG_POISONED':
      self.hp -= 25 
    elif response and 'SCREAMED' in response:
      # Response like W{row}{col}_SCREAMED
      shoot_pos = (int(response[1]), int(response[2]))
      self.kb.difference_update(set([f'S{pos[0]}{pos[1]}' for pos in get_adj_pos(shoot_pos, map_size)])) 
      self.kb.add(f'!W{shoot_pos[0]}{shoot_pos[1]}')
    elif response and 'FELL' in response:
      # Response like A{row}{col}_FELL
      shoot_pos = (int(response[1]), int(response[2]))
      self.kb.add(f'!W{shoot_pos[0]}{shoot_pos[1]}')
  
  def percept(self, info: list[str], map_size: int):
    # Get info and add knowledge to knowledge base
    adj_pos = get_adj_pos(self.pos, map_size)
    for i in info:
      if i == 'G' or i == 'H_P':
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}")
      elif i in percept_map.values():
        obj = list(percept_map.keys())[list(percept_map.values()).index(i)]
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}")
      elif i[1:] in percept_map.values():
        obj = list(percept_map.keys())[list(percept_map.values()).index(i[1:])]
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}")
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}->{'&'.join([f'!{obj}{pos[0]}{pos[1]}' for pos in adj_pos])}")

  def think(self, map_size):
    # Grab when possible
    if f'G{self.pos[0]}{self.pos[1]}' in self.kb or f'H_{self.pos[0]}{self.pos[1]}' in self.kb:
      self.intention.append('GRAB')

    # Infer safe cells from knowledge base
    adj_pos = [pos for pos in get_adj_pos(self.pos, map_size) if pos not in {*self.explored_cells, *self.safe_cells}]
    for pos in adj_pos:
      if tt_entail(self.kb, f'!W{pos[0]}{pos[1]}&!P{pos[0]}{pos[1]}&!P_G{pos[0]}{pos[1]}', pos):
        self.safe_cells.add(pos)
      elif tt_entail(self.kb, f'!W{pos[0]}{pos[1]}&!P{pos[0]}{pos[1]}', pos):
        self.poison_cells.add(pos)

    # Find path to a cell
    flag = 'SAFE'
    check_cell_to_move = None
    if self.safe_cells.difference(self.explored_cells):
      check_cell_to_move = lambda cell: cell not in self.explored_cells
    elif [clause for clause in self.kb if clause[0] == 'S']:
      flag = 'SHOOT'
      check_cell_to_move = lambda cell: f'S{cell[0]}{cell[1]}' in self.kb
    else:
      flag = 'RETURN'
      check_cell_to_move = lambda cell: cell == (0, 0)

    path = find_path(self.pos, self.explored_cells, self.safe_cells, check_cell_to_move, map_size)

    # Make intention of moving to this cell
    temp_pos, temp_dir = self.pos, self.dir
    for i in range(len(path) - 1):
      cur, next = path[i], path[i + 1]
      # Rotate
      rotations = []
      if next[0] == cur[0]:
        if next[1] > cur[1]: rotations = rotate_map[f'{dir_map[temp_dir]}_RIGHT']
        elif next[1] < cur[1]: rotations = rotate_map[f'{dir_map[temp_dir]}_LEFT']
      elif next[1] == cur[1]:
        if next[0] > cur[0]: rotations = rotate_map[f'{dir_map[temp_dir]}_DOWN']
        elif next[0] < cur[0]: rotations = rotate_map[f'{dir_map[temp_dir]}_UP']
      for rotate in rotations:
        self.intention.append(rotate)
        if rotate == 'RIGHT': temp_dir = (temp_dir + 1) % 4
        elif rotate == 'LEFT': temp_dir = (4 + temp_dir - 1) % 4
      # Move
      self.intention.append('MOVE')
      offset = move_map[temp_dir]
      temp_pos = (temp_pos[0] + offset[0], temp_pos[1] + offset[1])

    # Extra action
    if flag == 'SHOOT':
      sus_pos = [pos for pos in get_adj_pos(temp_pos, map_size) if pos not in self.safe_cells and f'!W{pos[0]}{pos[1]}' not in self.kb]
      # Find min rotation
      intention_if_right, intention_if_left = [], []
      for i in range(4):
        if (temp_pos[0] + move_map[(temp_dir + i) % 4][0], temp_pos[1] + move_map[(temp_dir + i) % 4][1]) in sus_pos:
          intention_if_right.append('SHOOT')
          self.intention += intention_if_right
          break
        if (temp_pos[0] + move_map[(4 + temp_dir - i) % 4][0], temp_pos[1] + move_map[(4 + temp_dir - i) % 4][1]) in sus_pos:
          intention_if_left.append('SHOOT')
          self.intention += intention_if_left
          break
        intention_if_right.append('RIGHT')
        intention_if_left.append('LEFT')
    elif flag == 'RETURN':
      self.intention.append('CLIMB')