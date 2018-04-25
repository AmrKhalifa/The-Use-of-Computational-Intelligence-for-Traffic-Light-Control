from simulation import Simulator
from genetic_algorithms.genetic_tools import Chromosome
from genetic_algorithms.ga_static_traffic_actuator import StaticTrafficLightActuator
from genetic_algorithms.tripinfo_extract import XMLDataExtractor
from genetic_algorithms.genetic_tools import GAOpertations
import traci
import random
import matplotlib.pyplot as plt
import time
from stats.output_parser import SimulationOutputParser
import pandas as pd
import numpy as np

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
path = "tripinfo.xml"
fitness_list = []

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
    f1.set_index(index, inplace=True)
    f1.to_csv(file)

# ///////////////////////// initializing the population ///////////////////////////////////

time1 = time.time()
timing_list = []
for _ in range(5):
    timing_list.append(random.sample(range(1, 200), 8))
#simulation_time = 1000

population = []

 # initializing the chromosomes #
for timing in timing_list:

    chromosome = Chromosome(timing, fitness= 0)
    chromosome_controller = StaticTrafficLightActuator(chromosome)

    sim = Simulator()
    sim.add_tickable(chromosome_controller)
    sim.run(sumocfg1, gui=False)

    traci.close()

    fitness = XMLDataExtractor(path).get_data()
    chromosome.set_fitness(fitness)
    population.append(chromosome)

# population.sort(key=lambda x: x._fitness, reverse=True)
# print("the population is initialized ...")
# print(" the population is : ")
# for chromosome in population :
#     print(chromosome._phases_steps)
#     print(chromosome._fitness)
# print("*="*15)

# ///////////////////////////// carrying out GA operations /////////////////////////////
simulation_dataFrame = define_data_frame()

print(" performing genetic algorithm ....")
for i in range (0,4):
    print("iteration : ",i)
    ga_operator = GAOpertations()

    # crossover #

    rand1 = random.randint(0,4)
    rand2 = random.randint(0,4)
    offspring = ga_operator.corssover(population[rand1],population[rand2])
    #print("an offspring is born ")
    #print(offspring.get_data())

    # mutation on the offspring #

    mutated_offspring = ga_operator.mutate(offspring)
    #print("after mutation , the offspring is: ")
    #print(mutated_offspring.get_data())

    # acquiring offspring's fitness #

    offspring_chromosome_controller = StaticTrafficLightActuator(mutated_offspring)
    sim = Simulator()
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(offspring_chromosome_controller)
    sim.run(sumocfg1, gui=False)
    traci.close()

    mean_speed_result = (np.mean(sim.results['mean_speed']))
    duration_result = (np.mean(sim.results['duration']))
    waiting_time = (np.mean(sim.results['waiting_time']))
    time_loss =(np.mean(sim.results['time_loss']))

    iteration_dataFrame = generate_iteration_data_frame (i,mean_speed_result,duration_result,waiting_time,time_loss)

    simulation_dataFrame = concat_frames(simulation_dataFrame, iteration_dataFrame)

    fitness = XMLDataExtractor(path).get_data()
    mutated_offspring.set_fitness(fitness)
    #print(mutated_offspring.get_data())
    mutated_chromosome_data, mutated_chromosome_fitness = mutated_offspring.get_data()

    # survival of the fittest #

    for chromosome in population:
        if chromosome._fitness > mutated_chromosome_fitness:
            population.remove(max(population,key=lambda x: x._fitness ))
            population.append(mutated_offspring)
            break

    best_solution = min(population,key=lambda x: x._fitness )
    fitness_list.append(best_solution._fitness)



print("The fitness list is: ",fitness_list)
time2 = time.time()
plt.plot(fitness_list)
plt.show()
print("="*10)
print("iteration were performed in: ",time2-time1," seconds.")

save_dataframe2CSV(simulation_dataFrame,"iteration","ga_results.csv")

print(simulation_dataFrame.head())
# /////////////////////////////////////////////////////////////////////

