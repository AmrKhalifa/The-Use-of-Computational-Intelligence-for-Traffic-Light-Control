from reward import RewardCalculator
from simulation import Simulator
import numpy as np
from stats.output_parser import SimulationOutputParser
from gradient_descent.static_controller import StaticTrafficLightController
from action import PhaseModifier
sim = Simulator()

sim.add_simulation_component(SimulationOutputParser)
t = [3]*8
t[0] = 50
t[4] = 50
print(t)
controller = StaticTrafficLightController(PhaseModifier("node1"),list(range(8)),t)

sim.add_tickable(controller)



sumocfg1 = "..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
sumocfg2 = "..\\test_environments\\grid_map\\4by4.sumocfg"


sim.run(sumocfg1, gui=False)
print(sim.results["mean_speed"].var()**.5)
print(sim.results["duration"].var()**.5)
