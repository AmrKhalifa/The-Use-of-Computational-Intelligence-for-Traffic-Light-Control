from simulation import Simulator
import numpy as np
from action import PhaseModifier
from greedy.greedy_actor import LongestQueueFirst
from SARS import StateAction
from SARS import RewardCollector
from reward import RewardCalculator

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
roads_list = [["-road1_0","road3_0"],["road2_0","road4_0"]]

rc = RewardCalculator(alpha= 0)
rewardCollector = RewardCollector(rc)

sim = Simulator()
sim.add_simulation_component(StateAction)
sim.add_tickable(rc)
sim.add_tickable(rewardCollector)

sim.run(sumocfg1, gui=False)
sim.results['rewards'] = rewardCollector.get_reward_log()
states = (sim.results['state'])

print(sim.results['rewards'])



