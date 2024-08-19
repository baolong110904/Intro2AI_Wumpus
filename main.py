from program import Program
from agent import Agent

if __name__ == '__main__':
  program = Program('map2.txt')
  agent = Agent()

  map_size = program.map_size

  while True:
    info = program.report_cell(agent.pos)
    action = agent.act(info, map_size)

    # Handle UI base on this info
    if action: print(action)
    
    if action:
      response_info = program.verify_action(action)

      # Handle UI base on this info
      if response_info: print(response_info)

      if response_info == 'AGENT_CLIMBED' or response_info == 'AGENT_DIED' : break
      else: agent.react(response_info, map_size)

  print(f'POINT {program.point}')