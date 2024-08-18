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
      action_type = self.intention.pop(0)
      if action_type == 'MOVE':
        offset = move_map[self.dir]
        self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
      elif action_type == 'RIGHT':
        self.dir = (self.dir + 1) % 4
      elif action_type == 'LEFT':
        self.dir = (4 + self.dir - 1) % 4
      elif action_type == 'HEAL':
        if self.heal > 0:
          self.heal -= 1
          self.hp += 25
      self.explored_cells.add(self.pos)
      return action_type, self.pos, self.hp
    else:
      # If there is no pending action, create new
      self.percept(info, map_size)
      self.think(map_size)
  
  def verify_info(self, info):
    if info == 'HP_GRABED': self.heal += 1
    elif info == 'PG_ENTERED': self.hp -= 25 
  
  def percept(self, info: list[str], map_size: int):
    # Get info and add knowledge to knowledge base
    adj_pos = get_adj_pos(self.pos, map_size)
    for i in info:
      if i == 'G' or i == 'H_P':
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}")
        self.intention.append('GRAB')
      elif i in percept_map.values():
        obj = list(percept_map.keys())[list(percept_map.values()).index(i)]
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}")
      elif i[1:] in percept_map.values():
        obj = list(percept_map.keys())[list(percept_map.values()).index(i[1:])]
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}")
        self.kb.add(f"{i}{self.pos[0]}{self.pos[1]}->{'&'.join([f'!{obj}{pos[0]}{pos[1]}' for pos in adj_pos])}")

  def think(self, map_size):
    # Grab when possible
    if 'GRAB' not in self.intention and (f'G{self.pos[0]}{self.pos[1]}' in self.kb or f'H_{self.pos[0]}{self.pos[1]}' in self.kb):
      self.intention.append('GRAB')
    # Infer safe cells from knowledge base
    adj_pos = [pos for pos in get_adj_pos(self.pos, map_size) if pos not in {*self.explored_cells, *self.safe_cells}]
    for pos in adj_pos:
      if tt_entail(self.kb, f'!W{pos[0]}{pos[1]}&!P{pos[0]}{pos[1]}&!P_G{pos[0]}{pos[1]}', pos):
        self.safe_cells.add(pos)
      elif tt_entail(self.kb, f'!W{pos[0]}{pos[1]}&!P{pos[0]}{pos[1]}&P_G{pos[0]}{pos[1]}', pos):
        self.poison_cells.add(pos)
    # Make intention of moving to a safe cell
    return_flag = not self.safe_cells.difference(self.explored_cells)
    path = find_path(self.pos, self.explored_cells, self.safe_cells, self.poison_cells, map_size, return_flag)
    temp_dir = self.dir
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
    if return_flag:
      self.intention.append('CLIMB')