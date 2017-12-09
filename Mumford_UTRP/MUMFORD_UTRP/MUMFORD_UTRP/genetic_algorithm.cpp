#include<genetic.h>

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
	std::vector<int>dominated;
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
		while ((j = rand() % population_size) != i);
		RouteSet offspring_routeset = crossover(population_array[i].routeset, population_array[j].routeset);
		if (!repair(offspring_routeset, transit_network, max_route_length))
			continue;
		mutate(offspring_routeset, transit_network, min_route_length, max_route_length);
		Individual offspring = { offspring_routeset, fitness(offspring_routeset, transit_network,demand) };
		//if is duplicate continue
		if (dominates(offspring, population_array[i])) {
			dominated.push_back(i);
			new_generation[i] = offspring;
			continue;
		}
		if (dominates(offspring, population_array[j])) {
			dominated.push_back(j);
			new_generation[j] = offspring;
			continue;
		}
		if (offspring.fitness.first < best_so_far[0]) {
			if (best_so_far_indices[0] != i) {
				dominated.push_back(i);
				new_generation[i] = offspring;
				continue;
			}
			else {
				dominated.push_back(j);
				new_generation[j] = offspring;
				continue;
			}
		}
		if (offspring.fitness.second< best_so_far[1]) {
			if (best_so_far_indices[1] != i) {
				dominated.push_back(i);
				new_generation[i] = offspring;
				continue;
			}
			else {
				dominated.push_back(j);
				new_generation[j] = offspring;
				continue;
			}
		}
		if (dominates(population_array[j], offspring) && dominates(population_array[i], offspring))
			continue;
		else
			for (int k = 0; k < population_size; k++) {
				if (has_element(dominated, k))
					continue;
				if (dominates(offspring, population_array[k])) {
					dominated.push_back(k);
					new_generation[k] = offspring;
					continue;
				}
			}
		for (int k = 0; k < population_size; k++)
			if (has_element(dominated, k))
				population_array[k] = new_generation[k];

	}
	delete[] new_generation;
}