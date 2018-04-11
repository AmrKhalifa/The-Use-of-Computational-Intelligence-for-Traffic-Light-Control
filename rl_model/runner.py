from reward import RewardCalculator
from simulation import Simulator
from stats import OverallAverageSpeedRecorder


sim = Simulator()
rc = RewardCalculator()
#sim.add_tickable(rc)
sim.add_simulation_component(OverallAverageSpeedRecorder)

sumocfg1 = "..\\test_environments\\single_intersection_map\\newnet.sumocfg"
sumocfg2 = "..\\test_environments\\grid_map\\4by4.sumocfg"
sim.run(sumocfg1, time_steps=1000, gui=False)

