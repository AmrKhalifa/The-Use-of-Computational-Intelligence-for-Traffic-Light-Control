from reward import RewardCalculator
from simulation import Simulator
import numpy as np
from stats.output_parser import SimulationOutputParser


sim = Simulator()

sim.add_simulation_component(SimulationOutputParser)



sumocfg1 = "..\\test_environments\\single_intersection_map\\newnet.sumocfg"
sumocfg2 = "..\\test_environments\\grid_map\\4by4.sumocfg"


sim.run(sumocfg1, time_steps=1000, gui=False)
#sim.save_results("result1")
print(np.array(sim.results["time_loss"]).mean())
print(np.array(sim.results["duration"]).mean())
print(np.array(sim.results["mean_speed"]).mean())
print(np.array(sim.results["waiting_time"]).mean())