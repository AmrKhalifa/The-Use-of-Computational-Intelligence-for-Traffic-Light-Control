from reward import RewardCalculator
from simulation import Simulator
import numpy as np
from stats.output_parser import SimulationOutputParser


sim = Simulator()

sim.add_simulation_component(SimulationOutputParser)



sumocfg1 = "..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
sumocfg2 = "..\\test_environments\\grid_map\\4by4.sumocfg"


sim.run(sumocfg1, gui=False)
