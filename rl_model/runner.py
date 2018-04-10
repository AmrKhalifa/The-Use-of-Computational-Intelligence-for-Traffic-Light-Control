from reward import RewardCalculator
from simulation import Simulator

sim = Simulator()
rc = RewardCalculator()
#sim.add_tickable(rc)

sim.run("..\\test_environments\\single_intersection_map\\newnet.sumocfg", time_steps=1000, gui=False)

