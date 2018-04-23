from rl_model.simulation import Simulator
from rl_model.genetic_algorithms.genetic_tools import Chromosome
from rl_model.genetic_algorithms.ga_static_traffic_actuator import StaticTrafficLightAcuator
from rl_model.genetic_algorithms.tripinfo_extract import XMLDataExtractor
from rl_model.genetic_algorithms.genetic_tools import GAOpertations
import traci
import random

sumocfg1 = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
path =  "D:\My study\\5th year\\Graduation Project\\traffic-optimization\\rl_model\\genetic_algorithms\\tripinfo.xml"

timing1 = [100,100,100,100,100,100,100,100]
timing2 = [12.5,12.5,5,5,12.5,25,25,15]
timing3 = [10,10,10,10,15,15,15,15]
timing4 = [100,50,100,50,100,50,100,50]

simulation_time = 1000

# ///////////////////////// initializing the population ///////////////////////////////////


# ///////
first_chromosome = Chromosome(timing1,fitness =0)
first_chromosome_controller = StaticTrafficLightAcuator(first_chromosome,simulation_time)

second_chromosome = Chromosome(timing2,fitness =0)
second_chromosome_controller = StaticTrafficLightAcuator(second_chromosome,simulation_time)

third_chromosome = Chromosome(timing3,fitness =0)
third_chromosome_controller = StaticTrafficLightAcuator(third_chromosome,simulation_time)

forth_chromosome = Chromosome(timing4,fitness =0)
forth_chromosome_controller = StaticTrafficLightAcuator(forth_chromosome,simulation_time)

sim = Simulator()
sim.add_tickable(first_chromosome_controller)
sim.run(sumocfg1, time_steps=simulation_time, gui=False)
traci.close()
fitness = XMLDataExtractor(path).get_data()
first_chromosome.set_fitness(fitness)

sim = Simulator()
sim.add_tickable(second_chromosome_controller)
sim.run(sumocfg1, time_steps=simulation_time, gui=False)
traci.close()
fitness = XMLDataExtractor(path).get_data()
second_chromosome.set_fitness(fitness)

sim = Simulator()
sim.add_tickable(third_chromosome_controller)
sim.run(sumocfg1, time_steps=simulation_time, gui=False)
traci.close()
fitness = XMLDataExtractor(path).get_data()
third_chromosome.set_fitness(fitness)

sim = Simulator()
sim.add_tickable(forth_chromosome_controller)
sim.run(sumocfg1, time_steps=simulation_time, gui=False)
traci.close()
fitness = XMLDataExtractor(path).get_data()
forth_chromosome.set_fitness(fitness)

print(first_chromosome.get_data())
print(second_chromosome.get_data())
print(third_chromosome.get_data())
print(forth_chromosome.get_data())

population = []

population.append(first_chromosome)
population.append(second_chromosome)
population.append(third_chromosome)
population.append(forth_chromosome)

population.sort(key=lambda x: x._fitness, reverse=True)
print("the list is sorted")
print("the population is initialized ...")
print("=*"*10)

for chromosome in population :
    print(chromosome._phases_steps)
    print(chromosome._fitness)
print("*="*15)

for i in range (10):
    print("iternation : ",i)
    ga_operator = GAOpertations()
    print("an offspring is born ")
    rand1 = random.randint(0,3)
    rand2 = random.randint(0,3)
    offspring = ga_operator.corssover(population[rand1],population[rand2])
    print(offspring.get_data())

    mutated_offspring = ga_operator.mutate(offspring)
    print("the offspring is mutated ")
    print(mutated_offspring.get_data())


    offspring_chromosome_controller = StaticTrafficLightAcuator(mutated_offspring , simulation_time)
    sim = Simulator()
    sim.add_tickable(offspring_chromosome_controller)
    sim.run(sumocfg1, time_steps=simulation_time, gui=False)
    traci.close()
    fitness = XMLDataExtractor(path).get_data()
    mutated_offspring.set_fitness(fitness)
    print(mutated_offspring.get_data())
    mutated_chromosome_data, mutated_chromosome_fitness = mutated_offspring.get_data()


    for chromosome in population:
        if chromosome._fitness > mutated_chromosome_fitness:
            population.remove(max(population,key=lambda x: x._fitness ))
            population.append(mutated_offspring)
            break

    print("*="*10)
    print("the new population is :")
    for chromosome in population :
        print(chromosome._phases_steps)
        print(chromosome._fitness)

print("="*10)
print("the best solution is : ")
best_solution = min(population,key=lambda x: x._fitness )
print(best_solution.get_data())
# /////////////////////////////////////////////////////////////////////

