from program import Program
from agent import Agent

if __name__ == '__main__':
  program = Program('map1.txt')
  agent = Agent()

  map_size = program.map_size
  i = 0

  while True:
    info = program.report_cell(agent.pos)
    action = agent.act(info, map_size)

    # Handle UI base on this info
    if action: print(action[0])
    
    if action:
      # Handle UI base on this info
      response_info = program.verify_action(action)
      if response_info: print(response_info)

      if response_info == 'GAME_OVER': break
      else: agent.verify_info(response_info)

  print(f'POINT {program.point}')