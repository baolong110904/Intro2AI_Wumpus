percept_map = {
  'W': 'S',
  'P': 'B',
  'P_G': 'W_H',
  'H_P': 'G_L'
}

dir_map = {
  0: "RIGHT",
  1: "DOWN",
  2: "LEFT",
  3: "UP"
}

rotate_map = {
  **dict.fromkeys(['RIGHT_RIGHT', 'LEFT_LEFT', 'UP_UP', 'DOWN_DOWN'], []),
  **dict.fromkeys(['RIGHT_DOWN', 'DOWN_LEFT', 'LEFT_UP', 'UP_RIGHT'], ['RIGHT']),
  **dict.fromkeys(['RIGHT_UP', 'UP_LEFT', 'LEFT_DOWN', 'DOWN_RIGHT'], ['LEFT']),
  **dict.fromkeys(['RIGHT_LEFT', 'LEFT_RIGHT', 'UP_DOWN', 'DOWN_UP'], ['RIGHT', 'RIGHT']),
}

move_map = {
  0: (0, 1),
  1: (1, 0),
  2: (0, -1),
  3: (-1, 0)
}

def get_adj_pos(pos, map_size):
  offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  return [(pos[0] + offset[0], pos[1] + offset[1]) for offset in offsets if pos[0] + offset[0] in range(map_size) and pos[1] + offset[1] in range(map_size)]

def tt_entail(kb: set[str], alpha: str, pos: tuple[int, int]):
  # Only take clause involved to the inferred pos
  temp_kb = set([clause for clause in kb if f'{pos[0]}{pos[1]}' in clause])
  # Only take Q in P -> Q clauses if P true
  shorten_kb = set()
  for clause in temp_kb:
    if '->' not in clause:
      shorten_kb.add(clause)
    elif clause.split('->')[0] in kb:
      shorten_kb.add(clause.split('->')[1])
  # Only take involved clause in & series
  temp_kb = set(shorten_kb)
  shorten_kb = set()
  for clause in temp_kb:
    if '&' not in clause: shorten_kb.add(clause)
    else: shorten_kb.update(set([c for c in clause.split('&') if f'{pos[0]}{pos[1]}' in c]))
  # Extract symbols
  symbols = set()
  for clause in shorten_kb:
    s = clause.replace('|', ' ').replace('!', ' ').split(' ')
    symbols.update(set(s))
  s = alpha.replace('!', ' ').replace('&', ' ').split(' ')
  symbols.update(s)
  symbols = symbols.difference({''})
  # Checking
  return tt_check_all(shorten_kb, alpha, symbols, {})

def tt_check_all(kb: set[str], alpha: str, symbols: set[str], model: dict):
  if not symbols:
    is_kb_true = True
    for clause in kb:
      is_kb_true = is_kb_true and check_clause(clause, model)
    if is_kb_true:
      return check_clause(alpha, model)
    else:
      return True
  else:
    p = list(symbols)[0]
    rest = set(list(symbols)[1:])
    return tt_check_all(kb, alpha, rest, {**model, p: True}) and tt_check_all(kb, alpha, rest, {**model, p: False})

def check_clause(clause: str, model: dict):
  if '->' in clause:
    return check_clause('!' + clause.split('->')[0], model) or check_clause(clause.split('->')[1], model)
  elif '|' in clause:
    return any([check_clause(c, model) for c in clause.split('|')])
  elif '&'in clause:
    return all([check_clause(c, model) for c in clause.split('&')])
  elif '!' in clause:
    return not check_clause(clause[1:], model)
  else:
    return model[clause]

def find_path(
  current_cell: tuple[int, int],
  explored_cells: set[tuple[int, int]],
  safe_cells: set[tuple[int, int]],
  check,
  map_size: int,
):
  if check(current_cell): return [current_cell]
  frontier, cost, expanded, moves = [current_cell], [0], [], []
  # Loop
  while frontier:
    # Pick the min cost node
    min_cost = min(cost)
    cell = frontier.pop(cost.index(min_cost))
    cost.remove(min_cost)
    expanded.append(cell)
    # Check is goal
    if check(cell):
      moves = moves[:len(moves) - [m[1] for m in moves][::-1].index(cell)]
      moves.reverse()
      path = [*moves[0]]
      for fr, to in moves:
        if to == path[0]:
          path.insert(0, fr)
      return path
    # Expand
    adj_pos = [pos for pos in get_adj_pos(cell, map_size) if pos in {*explored_cells, *safe_cells} and pos not in expanded]
    for pos in adj_pos:
      pos_cost = min_cost + 1
      if pos not in frontier:
        frontier.append(pos)
        cost.append(pos_cost)
        moves.append((cell, pos))
      elif pos_cost < cost[frontier.index(pos)]:
        cost[frontier.index(pos)] = pos_cost
        moves.append((cell, pos))
  return[]

