from simulation import Simulator
from stats import SimulationOutputParser
from action import PhaseModifier
from static_controller import StaticTrafficLightController
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
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(controller)
    sim.run(sumocfg1, time_steps=1000, gui=False)
    objective = sim.results["mean_speed"].mean()
    return objective


def OI(old_objective, new_objective):
    return new_objective > old_objective


def IE(old_objective, new_objective):
    return new_objective >= old_objective

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

objective_history = []
current_timing = initial_timings()
previous_objective = evaluate_timing(current_timing)

for i in range(10):
    h = random.randrange(4)
    new_timings = llh(h, current_timing)
    objective = evaluate_timing(new_timings)
    if OI(previous_objective, objective):
        current_timing = new_timings
        previous_objective = objective
    objective_history.append(previous_objective)

print (current_timing)
plt.plot(objective_history)
plt.show()

