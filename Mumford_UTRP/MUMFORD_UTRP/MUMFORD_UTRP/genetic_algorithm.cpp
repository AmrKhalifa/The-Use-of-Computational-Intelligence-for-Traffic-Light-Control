#include<genetic.h>
#include<iostream>

void seed_population(Individual *population_array, int population_size, Graph &transit_network, int min_route_length,
																					int max_route_length, int n_routes, int *demand) {
	for (int i = 0; i < population_size; i++) {
		RouteSet rs= generate_random_routeset(transit_network, min_route_length, max_route_length, n_routes);
		auto fitness_ = fitness(rs, transit_network, demand);
		Individual indv = {rs, fitness_};
		population_array[i] = indv;
	}
}

bool dominates(Individual i1, Individual i2) {
	return (i1.fitness.first < i2.fitness.first && i1.fitness.second < i2.fitness.second);
}

void seamo_iterate(Individual *population_array, int population_size, Graph &transit_network, int min_route_length,
	int max_route_length, int n_routes, int *demand) {
	int *dominated = new int [population_size]();
	Individual *new_generation = new Individual[population_size];
	double best_so_far[2] = { INFINITY,INFINITY };
	int best_so_far_indices[2];
	for (int i = 0; i < population_size; i++) {
		if (population_array[i].fitness.first < best_so_far[0]) {
			best_so_far[0] = population_array[i].fitness.first;
			best_so_far_indices[0] = i;
		}
		if (population_array[i].fitness.second < best_so_far[1]) {
			best_so_far[1] = population_array[i].fitness.second;
			best_so_far_indices[1] = i;
		}
	}
	for (int i = 0; i < population_size; i++) {
		int j;
		while ((j = rand() % population_size) == i);
		RouteSet offspring_routeset = crossover(population_array[i].routeset, population_array[j].routeset);
		if (!repair(offspring_routeset, transit_network, max_route_length))
			continue;
		mutate(offspring_routeset, transit_network, min_route_length, max_route_length);
		Individual offspring = { offspring_routeset, fitness(offspring_routeset, transit_network,demand) };
		//if is duplicate continue TODO
		if (dominates(offspring, population_array[i])) {
			dominated[i] = 1;
			new_generation[i] = offspring;
			continue;
		}
		if (dominates(offspring, population_array[j])) {
			dominated[j] = 1;;
			new_generation[j] = offspring;
			continue;
		}
		if (offspring.fitness.first < best_so_far[0]) {
			if (best_so_far_indices[1] != i) {
				dominated[i] = 1;
				new_generation[i] = offspring;
				continue;
			}
			else {
				dominated[j] = 1;;
				new_generation[j] = offspring;
				continue;
			}
		}
		if (offspring.fitness.second< best_so_far[1]) {
			if (best_so_far_indices[0] != i) {
				dominated[i] = 1;
				new_generation[i] = offspring;
				continue;
			}
			else {
				dominated[j] = 1;
				new_generation[j] = offspring;
				continue;
			}
		}
		if (dominates(population_array[j], offspring) && dominates(population_array[i], offspring))
			continue;
		else
			for (int k = 0; k < population_size; k++) {
				if (dominated[k]==1)
					continue;
				if (dominates(offspring, population_array[k])) {
					dominated[k] = 1;
					new_generation[k] = offspring;
					continue;
				}
			}
	}
	for (int k = 0; k < population_size; k++)
		if (dominated[k] == 1)
			population_array[k] = new_generation[k];
	int n_new_offspring = 0;
	for (int i = 0; i < population_size; i++)
		n_new_offspring += dominated[i];
	std::cout << n_new_offspring << "\n";
	delete[] dominated;
	delete[] new_generation;
}