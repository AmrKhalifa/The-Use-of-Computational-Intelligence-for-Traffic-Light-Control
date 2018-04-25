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

sumocfg1 = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
path = "tripinfo.xml"
fitness_list = []
mean_speend_result = []
duration_result =[]
waiting_time = []
time_loss = []


# ///////////////////////// initializing the population ///////////////////////////////////

time1 = time.time()
timing_list = []
for _ in range(10):
    timing_list.append(random.sample(range(1, 200), 8))
simulation_time = 1000

population = []
simulation_dataFrame = pd.DataFrame({'iteration': [0],
                                    'mean_speed': [0],
                                       'duration': [0],
                                  'waiting_time': [0],
                                     'time_loss': [0]})
simulation_dataFrame.set_index('iteration',inplace= True)

 # initializing the chromosomes #
for timing in timing_list:

    chromosome = Chromosome(timing, fitness= 0)
    chromosome_controller = StaticTrafficLightActuator(chromosome,simulation_time)

    sim = Simulator()
    sim.add_tickable(chromosome_controller)
    sim.run(sumocfg1, time_steps=simulation_time, gui=False)



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
print(" performing genetic algorithm ....")
i =0
while(i<10):
    print("iteration : ",i)
    ga_operator = GAOpertations()

    # crossover #

    rand1 = random.randint(0,3)
    rand2 = random.randint(0,3)
    offspring = ga_operator.corssover(population[rand1],population[rand2])
    #print("an offspring is born ")
    #print(offspring.get_data())

    # mutation on the offspring #

    mutated_offspring = ga_operator.mutate(offspring)
    #print("after mutation , the offspring is: ")
    #print(mutated_offspring.get_data())

    # acquiring offspring's fitness #

    offspring_chromosome_controller = StaticTrafficLightActuator(mutated_offspring , simulation_time)
    sim = Simulator()
    parser = SimulationOutputParser(sim)
    sim.add_simulation_component(SimulationOutputParser)
    sim.add_tickable(offspring_chromosome_controller)
    if(sim.run(sumocfg1, time_steps=simulation_time, gui=False)):
        continue
    sim.save_results("single_iteration_result")


    mean_speend_result = (np.mean(np.array(sim.results['mean_speed'])))
    duration_result = (np.mean(np.array(sim.results['duration'])))
    waiting_time = (np.mean(np.array(sim.results['waiting_time'])))
    time_loss =(np.mean(np.array(sim.results['time_loss'])))

    iteration_dataFrame = pd.DataFrame(({'iteration': [i],
                                    'mean_speed': [mean_speend_result],
                                       'duration': [duration_result],
                                  'waiting_time': [waiting_time],
                                     'time_loss': [time_loss]}))


    frames = [simulation_dataFrame,iteration_dataFrame]
    simulation_dataFrame = pd.concat(frames)


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
    i+=1

simulation_dataFrame.set_index('iteration',inplace= True)
simulation_dataFrame.to_csv("ga_result.csv")

print("The fitness list is: ",fitness_list)
time2 = time.time()
plt.plot(fitness_list)
plt.show()
print("="*10)
print("iteration were performed in: ",time2-time1," seconds.")

print(simulation_dataFrame.head())
# /////////////////////////////////////////////////////////////////////

