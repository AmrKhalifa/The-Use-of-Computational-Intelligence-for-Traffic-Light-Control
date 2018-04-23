from rl_model.simulation import Simulator
from rl_model.stats import OverallAverageSpeedRecorder
from rl_model.action import PhaseModifier
from rl_model.gradient_descent.static_controller import StaticTrafficLightController
import matplotlib.pyplot as plt
import random

sumocfg1 = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
sumocfg2 = "..\\..\\test_environments\\grid_map\\4by4.sumocfg"
previous_objective = -1
timing = [30, 3, 30, 3]
def mutate_timing(timing, magnitue):
    n = len(timing)
    timing_to_modify = random.randrange(0,n)
    result = timing[:]
    result[timing_to_modify] += random.randrange(-magnitue, magnitue+1)
    result[timing_to_modify] = max(0, result[timing_to_modify])
    return result

objective_history = []
for i in range(100):
    new_timings = mutate_timing(timing,5)
    traffic_light = PhaseModifier("node1")
    controller = StaticTrafficLightController(controller=traffic_light, sequence=[4,3,0,3], timings=new_timings)
    sim = Simulator()
    sim.add_simulation_component(OverallAverageSpeedRecorder)
    sim.add_tickable(controller)
    sim.run(sumocfg1, time_steps=1000, gui=False)
    objective = sim.results["avg_speed"].mean()
    if objective > previous_objective:
        timing = new_timings
        previous_objective = objective
    objective_history.append(previous_objective)
print (timing)
plt.plot(objective_history)
plt.show()

