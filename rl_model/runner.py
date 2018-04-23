from reward import RewardCalculator
from simulation import Simulator
from stats import OverallAverageSpeedRecorder
from stats.mean_journey_time import OverallMeanJourneyTimeRecorder


sim = Simulator()
#rc = RewardCalculator()
#sim.add_tickable(rc)
#sim.add_simulation_component(OverallAverageSpeedRecorder)
#sim.add_simulation_component(OverallMeanJourneyTimeRecorder)

sumocfg1 = "..\\test_environments\\single_intersection_map\\newnet.sumocfg"
sumocfg2 = "..\\test_environments\\grid_map\\4by4.sumocfg"
sim.run(sumocfg1, time_steps=5000, gui=False) 