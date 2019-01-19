from simulation import Simulator
from stats import SimulationOutputParser
from action import PhaseModifier
from static_controller import StaticTrafficLightController
import matplotlib.pyplot as plt
import os
import random
import pandas as pd
import pickle

# /////////////////////////////////////////////////////////////////////////////////////////

from gradient_descent.random_descent import define_data_frame
from gradient_descent.random_descent import generate_iteration_data_frame, concat_frames, save_dataframe2CSV
from gradient_descent.random_descent import initial_timings, evaluate_timing, save_timing_performance, OI, llh
import random
import math

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
sumocfg2 = "..\\..\\test_environments\\grid_map\\4by4.sumocfg"


def simulated_annealing_accept(previous_objective, objective, temperature):
    if objective < previous_objective:
        return True
    if temperature < 0.00000001:
        return False
    accept_worse = math.exp((previous_objective - objective) / temperature) > random.random()
    return accept_worse



def run_10_sim_anneal():

    results_dir = os.path.dirname(__file__)
    results_dir = os.path.dirname(results_dir)
    results_dir = os.path.join(results_dir, "results")
    results_dir = os.path.join(results_dir, "simulated_annealing")
    for run in range(10):
        results = False
        T = 1
        alpha = 0.99
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
            if simulated_annealing_accept(previous_objective, objective, T):
                improved[h] += 1
                current_timing = new_timings
                previous_objective = objective
                results = new_results
            x = generate_iteration_data_frame(i, results["mean_speed"].mean(), results["duration"].mean(),
                                          results["waiting_time"].mean(), results["time_loss"].mean())
            metrics = concat_frames(metrics, x)
            T *= alpha
        heuristic_report = {"called": called, "improved": improved}
        save_dataframe2CSV(metrics, "iteration",os.path.join(results_dir,"rd_runtime" + str(run) + ".csv"))
        save_timing_performance(current_timing, os.path.join(results_dir,"rd_final_iteration" + str(run)))
        file_io = open(os.path.join(results_dir,r"rd_heuristic_report" + str(run) + ".pkl"), 'wb')
        pickle.dump(heuristic_report, file_io)
        file_io.close()
        file_io = open(os.path.join(results_dir,"rd_final_iteration_timings" + str(run) + ".txt"), "w")
        file_io.write(str(current_timing))
        file_io.close()


run_10_sim_anneal()