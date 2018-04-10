from reward import RewardCalculator
from simulation import Simulator



sim = Simulator()
rc = RewardCalculator()
sim.add_tickable(rc)

sumocfg1 = "..\\test_environments\\single_intersection_map\\newnet.sumocfg"
sumocfg2 = "..\\test_environments\\grid_map\\4by4.sumocfg"
sim.run(sumocfg2, time_steps=5000, gui=False)

