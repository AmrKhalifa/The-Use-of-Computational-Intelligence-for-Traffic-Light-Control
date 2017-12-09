#include<stdio.h>
#include <iostream>
#include<Graph.h>
#include<genetic.h>
#include<fstream>
#include<string>
#include<sstream>
#include<cstdlib>

#define DISTANCES_MAT_PATH "C:\\Users\\eltay\\Documents\\grad_project\\Mumford_UTRP\\CEC2013Supp\\Instances\\MandlTravelTimes.txt"
#define DEMAND_MAT_PATH "C:\\Users\\eltay\\Documents\\grad_project\\Mumford_UTRP\\CEC2013Supp\\Instances\\MandlDemand.txt"
int main() {
	srand(685);
	std::ifstream distances_file(DISTANCES_MAT_PATH);
	std::ifstream demand_file(DEMAND_MAT_PATH);
	std::string line;
	Graph transit_network;

	if (distances_file.is_open() ){
		getline(distances_file, line);
		std::istringstream iss(line);
		int number_of_vertices= 0;
		Vertex* v;
		while (iss) {
			std::string entry;
			iss >> entry;
			if (!entry.empty()) {
				v = new Vertex(number_of_vertices);
				number_of_vertices++;
				transit_network.add_vertex(v);
			}
		}
		distances_file.seekg(0, std::ios::beg);
		int i = 0;
		while (getline(distances_file, line)) {
			std::istringstream iss(line);
			
			for (int j = 0; j < i; j++) {
				std::string entry;
				iss >> entry;
				if (entry != "Inf" && entry != "0") {
					int distance = std::atoi(entry.data());
					Edge* e = new Edge(distance, transit_network.get_vertex_by_number(i), transit_network.get_vertex_by_number(j));
					transit_network.add_edge(e);
				}
			}
			getline(distances_file, line);// get the empty line
			i++;
		}
		int *demand_matrix = new int[number_of_vertices*number_of_vertices];
		for (int j = 0; j < number_of_vertices; j++) {
			getline(demand_file, line);
			std::istringstream iss(line);
			for (int k = 0; k < number_of_vertices; k++) {
				std::string entry;
				iss >> entry;
				demand_matrix[j*number_of_vertices + k] = std::atoi(entry.data());
			}	
			getline(demand_file, line); // get the empty line
		}
		int population_size = 200, min_route_length = 2, max_route_length = 8, n_routes = 6;
		Individual *population = new Individual[population_size];
		//RouteSet rs = generate_random_routeset(transit_network, min_route_length, max_route_length, n_routes);
		seed_population(population, population_size, transit_network, min_route_length, max_route_length, n_routes, demand_matrix);
		for (int i = 0; i < 200; i++) {
			seamo_iterate(population, population_size, transit_network, min_route_length, max_route_length, n_routes, demand_matrix);
			std::cout << "Generation :" << i << "\n";
		}
		double best_so_far[2] = { INFINITY,INFINITY };
		int best_so_far_indices[2];
		for (int i = 0; i < population_size; i++) {
			if (population[i].fitness.first < best_so_far[0]) {
				best_so_far[0] = population[i].fitness.first;
				best_so_far_indices[0] = i;
			}
			if (population[i].fitness.second < best_so_far[1]) {
				best_so_far[1] = population[i].fitness.second;
				best_so_far_indices[1] = i;
			}
		}
		std::cout << population[best_so_far_indices[0]].routeset.to_string() << "\n";
		std::cout << population[best_so_far_indices[0]].fitness.first<<"\t"<< population[best_so_far_indices[0]].fitness.second<< "\n";

		std::cout << population[best_so_far_indices[1]].routeset.to_string() << "\n";
		std::cout << population[best_so_far_indices[1]].fitness.first << "\t" << population[best_so_far_indices[0]].fitness.second << "\n";
		int x;
		std::cin >> x;

	}

}