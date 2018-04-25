from simulation import Simulator
from stats import SimulationOutputParser
from action import PhaseModifier
from static_controller import StaticTrafficLightController
import matplotlib.pyplot as plt
import random

import pickle

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
sumocfg2 = "..\\..\\test_environments\\grid_map\\4by4.sumocfg"


def initial_timings():
    return [30]*8


def evaluate_timing(timing):
    traffic_light = PhaseModifier("node1")
    controller = StaticTrafficLightController(controller=traffic_light, sequence=list(range(8)), timings=timing)
    sim = Simulator()
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(controller)
    sim.run(sumocfg1, gui=False)
    return sim.results


def OI(old_objective, new_objective):
    return new_objective < old_objective


def IE(old_objective, new_objective):
    return new_objective <= old_objective

def llh(h, timing):
    if h==0:
        return mutate_timing(timing,5)
    elif h==1:
        return mutate_timings2(timing,2)
    elif h==2:
        return mutate_timings3(timing,1)
    elif h==3:
        return mutate_timings4(timing)

def mutate_timing(timings, magnitude):
    n = len(timings)
    timing_to_modify = random.randrange(0,n)
    result = timings[:]
    result[timing_to_modify] += random.randrange(-magnitude, magnitude+1)
    result[timing_to_modify] = max(0, result[timing_to_modify])
    return result


def mutate_timings2(timings, magnitude):
    n = len(timings)
    result = timings[:]
    for i in range(2):
        timing_to_modify = random.randrange(0, n)
        result[timing_to_modify] += random.randrange(-magnitude, magnitude + 1)
        result[timing_to_modify] = max(0, result[timing_to_modify])
    return result


def mutate_timings3(timings, magnitude):
    #select at random n cells and and mutate them
    n = len(timings)
    number_of_indices_to_perturb = random.randrange(n)
    indices_to_perturb = random.sample(range(n), number_of_indices_to_perturb)
    new_timings = timings[:]
    for i in indices_to_perturb:
        new_timings[i] += random.randrange(-magnitude, magnitude +1)
        new_timings[i] = max(0, new_timings[i])
    return new_timings


def mutate_timings4(timings):
    n = len(timings)
    new_timings = timings[:]
    a,b = random.sample(range(n), 2)
    new_timings[a], new_timings[b] = new_timings[b], new_timings[a]
    return new_timings

current_timing = initial_timings()
results = evaluate_timing(current_timing)
previous_objective = results["waiting_time"].mean()

metrics = {"mean_speed": [], "duration": [], "waiting_time": [], "time_loss": []}
improved = {0: 0, 1: 0, 2: 0, 3: 0}
called = {0: 0, 1: 0, 2: 0, 3: 0}

for i in range(3):
    h = random.randrange(4)
    new_timings = llh(h, current_timing)
    new_results = evaluate_timing(new_timings)
    objective = new_results["duration"].mean()
    called[h] += 1
    if OI(previous_objective, objective):
        improved[h] += 1
        current_timing = new_timings
        previous_objective = objective
        results = new_results
    for metric in metrics.keys():
        metrics[metric].append(results[metric].mean())

heuristic_report = {"called":called, "improved": improved}
print (heuristic_report)
plt.plot(metrics["duration"])
plt.show()