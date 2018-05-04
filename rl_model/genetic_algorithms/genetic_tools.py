import random


class Chromosome(object):
    def __init__(self, phases_steps,fitness):
        self._phases_steps = phases_steps
        self._fitness = fitness

    def set_fitness(self, fitness):
        self._fitness = fitness

    def get_data(self):
        return self._phases_steps,self._fitness


class GAOpertations(object):
    def __init__(self):
        pass

    def select_ranked(self,population):
        population.sort(key=lambda x: x._fitness, reverse=True)
        return population[0],population[1]
        pass

    def select_simply(self,population):
        rand1 = random.randint(0, len(population) - 1)
        rand2 = random.randint(0, len(population) - 1)
        return population[rand1], population[rand2]


    def point_corssover(self,first_chromosome,second_chromosome):

        portion = random.randint(0,len(first_chromosome._phases_steps))
        first_part = first_chromosome._phases_steps[:portion]
        second_part = second_chromosome._phases_steps[portion:]

        return Chromosome(first_part + second_part,fitness=0)


    def uniform_corssover(self,first_chromosome,second_chromosome):

        phase_steps = []
        for i in range(len(first_chromosome._phases_steps)):
            rand = bool(random.randint(0,1))
            if(rand):
                phase_steps.append(first_chromosome._phases_steps[i])
            else:
                phase_steps.append(second_chromosome._phases_steps[i])
        return Chromosome(phase_steps,fitness=0)


    def mutate(self,chromosome):

        mutated_chromosome = chromosome._phases_steps

        mutation_position = random.randint(0,len(mutated_chromosome)-1)
        plus_minus = bool(random.randint(0,1))

        if(plus_minus):
            mutated_chromosome[mutation_position] += random.randint(0,15)
        else:
            if mutated_chromosome[mutation_position] >10 :
                mutated_chromosome[mutation_position] -= random.randint(0,10)
            elif mutated_chromosome[mutation_position] > 5 and mutated_chromosome[mutation_position]< 10 :
                mutated_chromosome[mutation_position] -= random.randint(0, 5)
            else:
                mutated_chromosome[mutation_position] = 0

        return Chromosome(mutated_chromosome,fitness = 0)

