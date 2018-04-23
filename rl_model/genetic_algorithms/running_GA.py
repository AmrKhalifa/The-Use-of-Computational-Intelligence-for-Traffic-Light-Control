from rl_model.simulation import Simulator
from rl_model.genetic_algorithms.genetic_tools import Chromosome
from rl_model.genetic_algorithms.ga_static_traffic_actuator import StaticTrafficLightActuator
from rl_model.genetic_algorithms.tripinfo_extract import XMLDataExtractor
from rl_model.genetic_algorithms.genetic_tools import GAOpertations
import traci
import random
import matplotlib.pyplot as plt

sumocfg1 = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
path = "D:\My study\\5th year\\Graduation Project\\traffic-optimization\\rl_model\\genetic_algorithms\\tripinfo.xml"
fitness_list = []

# ///////////////////////// initializing the population ///////////////////////////////////

timing_list = []
for _ in range(10):
    timing_list.append(random.sample(range(1, 200), 8))
simulation_time = 1000

population = []

 # initializing the chromosomes #
for timing in timing_list:

    chromosome = Chromosome(timing, fitness= 0)
    chromosome_controller = StaticTrafficLightActuator(chromosome,simulation_time)
    sim = Simulator()
    sim.add_tickable(chromosome_controller)
    sim.run(sumocfg1, time_steps=simulation_time, gui=False)
    traci.close()
    fitness = XMLDataExtractor(path).get_data()
    chromosome.set_fitness(fitness)
    population.append(chromosome)

population.sort(key=lambda x: x._fitness, reverse=True)
print("the population is initialized ...")
print(" the population is : ")
for chromosome in population :
    print(chromosome._phases_steps)
    print(chromosome._fitness)
print("*="*15)

# ///////////////////////////// carrying out GA operations /////////////////////////////
print(" performing genetic algorithm ....")
for i in range (1000):
    print("iteration : ",i)
    ga_operator = GAOpertations()

    # crossover #

    rand1 = random.randint(0,3)
    rand2 = random.randint(0,3)
    offspring = ga_operator.corssover(population[rand1],population[rand2])
    print("an offspring is born ")
    print(offspring.get_data())

    # mutation on the offspring #

    mutated_offspring = ga_operator.mutate(offspring)
    print("after mutation , the offspring is: ")
    print(mutated_offspring.get_data())

    # acquiring offspring's fitness #

    offspring_chromosome_controller = StaticTrafficLightActuator(mutated_offspring , simulation_time)
    sim = Simulator()
    sim.add_tickable(offspring_chromosome_controller)
    sim.run(sumocfg1, time_steps=simulation_time, gui=False)
    traci.close()
    fitness = XMLDataExtractor(path).get_data()
    mutated_offspring.set_fitness(fitness)
    print(mutated_offspring.get_data())
    mutated_chromosome_data, mutated_chromosome_fitness = mutated_offspring.get_data()

    # survival of the fittest #

    for chromosome in population:
        if chromosome._fitness > mutated_chromosome_fitness:
            population.remove(max(population,key=lambda x: x._fitness ))
            population.append(mutated_offspring)
            break

    # printing the resulting gene pool of this iteration #

    print("*="*10)
    print("the new population is :")
    for chromosome in population :
        print(chromosome._phases_steps)
        print(chromosome._fitness)
    best_solution = min(population, key=lambda x: x._fitness)
    fitness_list.append(best_solution._fitness)

# printing the fittest specimen #

print("="*10)
print("the best solution is : ")
best_solution = min(population,key=lambda x: x._fitness )
print(best_solution.get_data())
fitness_list.append(best_solution._fitness)
plt.plot(fitness_list)
plt.show()
print("="*10)
# /////////////////////////////////////////////////////////////////////

