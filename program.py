from utils import *

class Program:
  def __init__(self, map_input: str):
    self.point = 0
    self.map = []
    # Initialize map
    with open(map_input) as file:
      # Read input
      self.map_size = int(file.readline())
      self.map = [line.strip().split('.') for line in file.readlines()]
      # Fill in object
      for row in range(self.map_size):
        for col in range(self.map_size):
          cell = self.map[row][col]
          self.map[row][col] = []
          if 'P_G' in cell:
            cell = cell.replace('P_G', '')
            self.map[row][col].append('P_G')
          if 'H_P' in cell:
            cell = cell.replace('H_P', '')
            self.map[row][col].append('H_P')
          if 'W' in cell:
            cell = cell.replace('W', '')
            self.map[row][col].append('W')
          if 'P' in cell:
            cell = cell.replace('P', '')
            self.map[row][col].append('P')
          if 'G' in cell:
            cell = cell.replace('G', '')
            self.map[row][col].append('G')
      # Fill in percept
      for row in range(self.map_size):
        for col in range(self.map_size):
          adj_pos = get_adj_pos((row, col), self.map_size)
          for obj in self.map[row][col]:
            if obj in percept_map.keys():
              for pos in adj_pos:
                self.map[pos[0]][pos[1]].append(percept_map[obj])
      
  def report_cell(self, pos: tuple[int, int]):
    # All info init with false value
    temp_info = ['!' + k for k in percept_map.keys()] + ['!' + v for v in percept_map.values()] + ['!G']
    info = [*temp_info]
    # Update to true if exist
    for item in self.map[pos[0]][pos[1]]:
      info[temp_info.index('!' + item)] = item
    return info
  
  def verify_action(self, action: str):
    if 'MOVE' in action:
      # Action like MOVE_{row}_{col}_{hp}
      _, row, col, hp = action.split('_')
      cell_info = self.map[int(row)][int(col)]
      if 'P' in cell_info or 'W' in cell_info:
        self.point -= 10000
        return 'AGENT_DIED'
      if 'P_G' in cell_info:
        if int(hp) - 25 <= 0:
          self.point -= 10000
          return 'AGENT_DIED'
        else: return 'PG_POISONED'
      self.point -= 10
    elif 'GRAB' in action:
      # Action like GRAB_{row}_{col}
      _, row, col = action.split('_')
      cell_info = self.map[int(row)][int(col)]
      if 'G' in cell_info:
        self.map[int(row)][int(col)].pop(self.map[int(row)][int(col)].index('G'))
        self.point += 5000
        return 'G_EXIST'
      if 'H_P' in cell_info:
        self.map[int(row)][int(col)].pop(self.map[int(row)][int(col)].index('H_P'))
        for pos in get_adj_pos((int(row), int(col)), self.map_size):
          self.map[pos[0]][pos[1]].pop(self.map[pos[0]][pos[1]].index('G_L'))
        return 'HP_EXIST'
      self.point -= 10
    elif 'SHOOT' in action:
      # Action like GRAB_{row}_{col}
      _, row, col = action.split('_')
      cell_info = self.map[int(row)][int(col)]
      self.point -= 100
      if 'W' in cell_info:
        self.map[int(row)][int(col)].pop(self.map[int(row)][int(col)].index('W'))
        for pos in get_adj_pos((int(row), int(col)), self.map_size):
          self.map[pos[0]][pos[1]].pop(self.map[pos[0]][pos[1]].index('S'))
        return f'W{row}{col}_SCREAMED'
      else:
        return f'A{row}{col}_FELL'
    elif 'CLIMB' in action:
      # Action like CLIMB_{row}_{col}
      _, row, col = action.split('_')
      if row == '0' and col == '0':
        self.point += 10
        return 'AGENT_CLIMBED'
      self.point -= 10
    else:
      self.point -= 10