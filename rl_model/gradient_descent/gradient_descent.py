from rl_model.simulation import Simulator
from rl_model.stats import OverallAverageSpeedRecorder
from rl_model.action import PhaseModifier
from rl_model.gradient_descent.static_controller import StaticTrafficLightController
import matplotlib.pyplot as plt
import random


sumocfg1 = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
sumocfg2 = "..\\..\\test_environments\\grid_map\\4by4.sumocfg"

def initial_timings():
    return [30, 3, 30, 3]

def evaluate_timing(timing):
    traffic_light = PhaseModifier("node1")
    controller = StaticTrafficLightController(controller=traffic_light, sequence=[4,3,0,3], timings=timing)
    sim = Simulator()
    sim.add_simulation_component(OverallAverageSpeedRecorder)
    sim.add_tickable(controller)
    sim.run(sumocfg1, time_steps=1000, gui=False)
    objective = sim.results["avg_speed"].mean()
    return objective

def OI(old_objective, new_objective):
    return new_objective > old_objective

def IE(old_objective, new_objective):
    return new_objective >= old_objective

def llh(h, timing):
    if (h==0):
        return mutate_timing(timing,5)
    elif (h==1):
        return mutate_timings2(timing,1)

def mutate_timing(timing, magnitude):
    n = len(timing)
    timing_to_modify = random.randrange(0,n)
    result = timing[:]
    result[timing_to_modify] += random.randrange(-magnitude, magnitude+1)
    result[timing_to_modify] = max(0, result[timing_to_modify])
    return result


def mutate_timings2(timings, magnitude):
    n = len(timing)
    result = timing[:]
    for i in range(2):
        timing_to_modify = random.randrange(0, n)
        result[timing_to_modify] += random.randrange(-magnitude, magnitude + 1)
        result[timing_to_modify] = max(0, result[timing_to_modify])
    return result


def mutate_timings3(timings):
    #select at random n cells and and mutate them
    pass


def mutate_timings4(timings):
        pass
    # swap two timings

objective_history = []

timing = initial_timings()
previous_objective = evaluate_timing(timing)

for i in range(100):
    h = random.choice([0, 1])

    new_timings = llh(h, timing)
    objective = evaluate_timing(new_timings)
    if OI(previous_objective, objective):
        print("improved")
        timing = new_timings
        previous_objective = objective
    objective_history.append(previous_objective)

print (timing)
plt.plot(objective_history)
plt.show()