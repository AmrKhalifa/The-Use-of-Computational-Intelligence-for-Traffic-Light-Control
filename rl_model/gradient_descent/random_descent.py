from simulation import Simulator
from stats import SimulationOutputParser
from action import PhaseModifier
from static_controller import StaticTrafficLightController
import matplotlib.pyplot as plt
import os
import random
import pandas as pd
import pickle


sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
sumocfg2 = "..\\..\\test_environments\\grid_map\\4by4.sumocfg"

# /////////////////////////////////////////////////////////////////////////////////////////

def define_data_frame():
    simulation_dataFrame = pd.DataFrame({'iteration': [0],
                                         'mean_speed': [0],
                                         'duration': [0],
                                         'waiting_time': [0],
                                         'time_loss': [0]})
    simulation_dataFrame.set_index('iteration', inplace=True)
    return simulation_dataFrame


def generate_iteration_data_frame(iteration_no,mean_speed_result,duration_result,waiting_time,time_loss):
    iteration_dataFrame = pd.DataFrame(({'iteration': [iteration_no],
                                         'mean_speed': [mean_speed_result],
                                         'duration': [duration_result],
                                         'waiting_time': [waiting_time],
                                         'time_loss': [time_loss]}))
    iteration_dataFrame.set_index('iteration',inplace= True)
    return iteration_dataFrame


def concat_frames(f1,f2):
    frames = [f1, f2]
    frame = pd.concat(frames)
    return frame


def save_dataframe2CSV(f1,index,file):
    #f1.set_index(index, inplace=True)
    f1.to_csv(file)


def initial_timings():
    return random.sample(range(50,100), 4)


def evaluate_timing(timing):
    traffic_light = PhaseModifier("node1")
    full_timings = [3]*8
    full_timings[0] = timing[0]
    full_timings[4] = timing[1]
    controller = StaticTrafficLightController(controller=traffic_light, sequence=list(range(8)), timings=full_timings)
    sim = Simulator()
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(controller)
    if not sim.run(sumocfg1, time_steps=2000, gui=False):
        return sim.results
    return False

def save_timing_performance(timing, filename):
    full_timings = [3]*8
    full_timings[0] = timing[0]
    full_timings[4] = timing[1]
    traffic_light = PhaseModifier("node1")
    controller = StaticTrafficLightController(controller=traffic_light, sequence=list(range(8)), timings=full_timings)
    sim = Simulator()
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(controller)
    sim.run(sumocfg1, gui=False)
    sim.save_results(filename)

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
    timing_to_modify = random.randrange(0, n)
    result[timing_to_modify] += random.choice([-10, 10])
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

def run_10_rand_desc():
    results_dir = os.path.dirname(__file__)
    results_dir = os.path.dirname(results_dir)
    results_dir = os.path.join(results_dir, "results")
    results_dir = os.path.join(results_dir, "random_descent")
    for run in range(10):
        results = False
        while not results:
            print("generating initial timings")
            current_timing = initial_timings()
            results = evaluate_timing(current_timing)
        previous_objective = results["duration"].mean()
        metrics = define_data_frame()
        improved = {0: 0, 1: 0, 2: 0, 3: 0}
        called = {0: 0, 1: 0, 2: 0, 3: 0}
        for i in range(1000):
            new_results = False
            while not new_results:
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
            x = generate_iteration_data_frame(i, results["mean_speed"].mean(), results["duration"].mean(),
                                          results["waiting_time"].mean(), results["time_loss"].mean())
            metrics = concat_frames(metrics, x)

        heuristic_report = {"called": called, "improved": improved}
        save_dataframe2CSV(metrics, "iteration",os.path.join(results_dir,"rd_runtime" + str(run) + ".csv"))
        save_timing_performance(current_timing, os.path.join(results_dir,"rd_final_iteration" + str(run)))
        file_io = open(os.path.join(results_dir,r"rd_heuristic_report" + str(run) + ".pkl"), 'wb')
        pickle.dump(heuristic_report, file_io)
        file_io.close()
        file_io = open(os.path.join(results_dir,"rd_final_iteration_timings" + str(run) + ".txt"), "w")
        file_io.write(str(current_timing))
        file_io.close()

