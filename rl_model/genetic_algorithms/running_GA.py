import random
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import traci
from action import PhaseModifier
from genetic_algorithms.ga_static_traffic_actuator import StaticTrafficLightActuator
from genetic_algorithms.genetic_tools import Chromosome
from genetic_algorithms.genetic_tools import GAOpertations
from genetic_algorithms.tripinfo_extract import XMLDataExtractor
from gradient_descent.static_controller import  StaticTrafficLightController
from simulation import Simulator
from stats.output_parser import SimulationOutputParser

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
path = "tripinfo.xml"
fitness_list = []
timings_list_ = []

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


def save_dataframe2CSV(f1,file):
    f1.to_csv(file)

#/////////////////////////////////////////////////////////////////////////////////////////////////



for iteration in range (10):

    # ///////////////////////// initializing the population ///////////////////////////////////


    simulation_dataFrame = define_data_frame()

    time1 = time.time()
    timing_list = []

    for _ in range(5):
        timing_list.append(random.sample(range(50, 100), 2))

    population = []

     # initializing the chromosomes #
    for timing in timing_list:

        print(timing)
        chromosome = Chromosome(timing, fitness= 0)
        configuration = []
        for ii in range (8):
            configuration.append(3)
            if ii == 0:
                configuration[ii] = timing [0]
            if ii == 4:
                configuration[ii] = timing [1]
        chromosome_controller = StaticTrafficLightController(PhaseModifier("node1"),list(range(0,8)),configuration)
        print(chromosome._phases_steps)
        print(configuration)

        sim = Simulator()
        sim.add_tickable(chromosome_controller)
        sim.run(sumocfg1, gui=False)

        fitness = XMLDataExtractor(path).get_data()
        chromosome.set_fitness(fitness)
        population.append(chromosome)

    for member in population:
        print(member._fitness)


    best_initial_solution = min(population, key=lambda x: x._fitness)

    configuration = []
    for ii in range(8):
        configuration.append(3)
        if ii == 0:
            configuration[ii] = best_initial_solution._phases_steps[0]
        if ii == 4:
            configuration[ii] = best_initial_solution._phases_steps[1]

    best_initial_solution_controller = StaticTrafficLightController(PhaseModifier("node1"), list(range(0,8)),configuration)
    sim = Simulator()
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(best_initial_solution_controller)
    sim.run(sumocfg1, gui=False)

    fitness = XMLDataExtractor(path).get_data()
    best_initial_solution.set_fitness(fitness)
    print("fitness of the best is: " ,fitness)

    mean_speed_result = (np.mean(sim.results['mean_speed']))
    duration_result = (np.mean(sim.results['duration']))
    waiting_time = (np.mean(sim.results['waiting_time']))
    time_loss = (np.mean(sim.results['time_loss']))
    iteration_dataFrame = generate_iteration_data_frame(0, mean_speed_result, duration_result, waiting_time, time_loss)

    simulation_dataFrame = concat_frames(simulation_dataFrame, iteration_dataFrame)


    # ///////////////////////////// carrying out GA operations /////////////////////////////

    print("*="*15)
    print("performing genetic algorithm ....")

    i = 0
    j = 0

    while i < 1000:

        print("iteration: ", i)
        ga_operator = GAOpertations()

        chromosome_1, chromosome_2 = ga_operator.select_simply(population)

        # crossover #

        offspring = ga_operator.point_corssover(chromosome_1,chromosome_2)

        # mutation on the offspring #

        mutated_offspring = ga_operator.mutate(offspring)

        # determining offspring's fitness #
        configuration = []


        for ii in range(8):
            configuration.append(3)
            if ii == 0:
                configuration[ii] = mutated_offspring._phases_steps[0]
            if ii == 4:
                configuration[ii] = mutated_offspring._phases_steps[1]


        offspring_chromosome_controller = StaticTrafficLightController(PhaseModifier("node1"), list(range(0, 8)),configuration)
        sim = Simulator()
        sim.add_simulation_component(SimulationOutputParser)
        sim.add_tickable(offspring_chromosome_controller)

        sim.run(sumocfg1, gui=False)

        fitness = XMLDataExtractor(path).get_data()
        mutated_offspring.set_fitness(fitness)

        print("the offspring's fitness is: ", mutated_offspring._fitness)

        # survival of the fittest #

        best_solution = min(population, key=lambda x: x._fitness)

        for chromosome in population:
            if chromosome._fitness > mutated_offspring._fitness:
                population.remove(max(population, key=lambda x: x._fitness))
                population.append(mutated_offspring)
                break


        if mutated_offspring._fitness < best_solution._fitness:

            mean_speed_result = (np.mean(sim.results['mean_speed']))
            duration_result = (np.mean(sim.results['duration']))
            waiting_time = (np.mean(sim.results['waiting_time']))
            time_loss = (np.mean(sim.results['time_loss']))

            j+=1
            iteration_dataFrame = generate_iteration_data_frame(j, mean_speed_result, duration_result, waiting_time,
                                                                    time_loss)

            simulation_dataFrame = concat_frames(simulation_dataFrame, iteration_dataFrame)

        else:
            j+=1
            simulation_dataFrame.tail(1)['iteration']=j
            simulation_dataFrame = concat_frames(simulation_dataFrame,simulation_dataFrame.tail(1))


        best_solution = min(population, key=lambda x: x._fitness)
        fitness_list.append(best_solution._fitness)
        timings_list_.append(best_solution._phases_steps)

        i += 1

    print("The fitness list is: ",fitness_list)
    timings_array = np.asarray(timings_list_)
    np.savetxt(str("timings_list"+str(iteration)+".csv"),timings_array, delimiter=",")

    time2 = time.time()
    #plt.plot(fitness_list)
    #plt.show()
    print("="*10)

    print("iteration were performed in: ",time2-time1," seconds.")
    sim.save_results("ga_results"+str(iteration))
    save_dataframe2CSV(simulation_dataFrame,"ga_results"+str(iteration)+".csv")

    print(simulation_dataFrame.head())
# /////////////////////////////////////////////////////////////////////
