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

    def corssover(self,first_chromosome,second_chromosome):
        portion = random.randint(0,7)
        first_part = first_chromosome._phases_steps[:portion]
        second_part = second_chromosome._phases_steps[portion:]

        return Chromosome(first_part + second_part,fitness=0)


    def mutate(self,chromosome):

        mutated_chromosome = chromosome._phases_steps

        mutation_position = random.randint(0,7)
        plus_minus = bool(random.randint(0,1))

        if(plus_minus):
            mutated_chromosome[mutation_position] += 10
        else:
            if(mutated_chromosome[mutation_position] >10 ):
                mutated_chromosome[mutation_position]-= 10
            else :
                mutated_chromosome[mutation_position] = 0

        return Chromosome(mutated_chromosome,fitness=0)

    		 
