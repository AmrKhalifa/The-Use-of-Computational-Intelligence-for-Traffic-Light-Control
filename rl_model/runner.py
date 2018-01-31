import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", "..\\test_environments\\grid_map\\4by4.sumocfg"]

import traci
from reward import RewardCalculator

rc = RewardCalculator()
traci.start(sumoCmd)
step = 0
while step < 10000:
    traci.simulationStep()
    rc.tick()
    rc.get_reward()

traci.close()