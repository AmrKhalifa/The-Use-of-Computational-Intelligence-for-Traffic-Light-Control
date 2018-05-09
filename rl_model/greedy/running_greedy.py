from simulation import Simulator
import numpy as np
from stats.output_parser import SimulationOutputParser
from action import PhaseModifier
from greedy.greedy_actor import LongestQueueFirst

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
roads_list = [["-road1_0","road3_0"],["road2_0","road4_0"]]

sim = Simulator()



LQF_actor = LongestQueueFirst("node1",roads_list)
sim.add_tickable(LQF_actor,freq=1)
sim.add_simulation_component(SimulationOutputParser)

sim.run(sumocfg1, gui=False)

mean_speed_result = (np.mean(sim.results['mean_speed']))
duration_result = (np.mean(sim.results['duration']))
waiting_time = (np.mean(sim.results['waiting_time']))
time_loss = (np.mean(sim.results['time_loss']))

print("×*×"*15)

print("Mean speed result: ", mean_speed_result)
print("duration result: ", duration_result)
print("waiting time result: ", waiting_time)
print("time loss result: ", time_loss)

